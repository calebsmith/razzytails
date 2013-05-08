import os
import json

import pygame

from yape.utils import validate_data_against_schema
from const import IMAGES_DIR, FONTS_DIR


def load_image(filename):
    image_file = os.path.join(IMAGES_DIR, filename)
    try:
        image = pygame.image.load(image_file).convert_alpha()
    except (IOError, pygame.error):
        print 'Image file {0} not found'.format(image_file)
        image = None
    return (filename, image)


def load_font(filename, font_size=16):
    font_file = os.path.join(FONTS_DIR, filename)
    try:
        font = pygame.font.Font(font_file, font_size)
    except (IOError, pygame.error):
        print 'Font file {0} not found'.format(font_file)
        font = None
    return (filename, font)


class Loader(object):
    """
    A simple base class that defines an interface for any classes that load
    content from the filesystem or a web-API. Defines only the load() method,
    which calls on load_contents and coerce_contents to load the external
    resource

    Subclasses must implement:
        load_contents - for loading raw content from a given location
        coerce_contents - for coercing the raw content into a python data
            structure, such as dictionaries and lists
    """

    def load(self, location):
        self.location = location
        return self.coerce_contents(self.load_contents(location))

    def load_contents(self, location):
        """
        Given a filename, or url, load data from the location and return its
        contents without modification
        """
        raise NotImplemented('Must be implemented in a subclass')

    def coerce_contents(self, contents):
        """
        Using data from `load_contents`, coerce the data into an internal
        structure of dictionaries and/or lists. (e.g. The simplest
        implementation is to use json.loads on JSON content)
        """
        raise NotImplemented('Must be implemented in a subclass')


class JSONFileLoader(Loader):
    """
    Retrieves data from a JSON file on the local filesystem. This is used as
    the default loader for LoadableAssets.
    """

    def load_contents(self, location):
        """
        Given a path/filename string as `location`, load data from that file in
        the local file system
        """
        if not location.endswith('.json'):
            location += '.json'
        try:
            f = open(location)
            return f.read()
        except IOError:
            print "File not found: {0}".format(location)
            return "{}"

    def coerce_contents(self, contents):
        """Parse the file as JSON"""
        try:
            return json.loads(contents)
        except ValueError:
            print "File {0} is not valid JSON".format(self.location)
            return {}


class BaseAsset(object):
    """
    A base class that defines methods common to the Asset and LoadableAsset
    classes.
    """

    def handle(self, data):
        """
        Handle data once it has been validated. By default, assigns values from
        data to attributes on self.
        """
        self._assign_to_self(data)

    def _assign_to_self(self, data):
        """Sets values from the data dictionary to the object itself"""
        for key, value in data.items():
            setattr(self, key, value)


class Asset(BaseAsset):
    """
    A game asset that is instantiated with data and does not load it directly.
    """

    def __init__(self, data=None):
        if data is not None:
            self.handle(data)


class LoadableAsset(BaseAsset):
    """
    A game asset or container of assets that is instatiated with a location,
    and loads data from that location to fill itself with asset objects.
    """

    def __init__(self, location=None, Loader=JSONFileLoader):
        # Determine what methods to call when validating individual fields
        self.field_validators = [
            getattr(self, attr)
            for attr in dir(self)
            if attr.startswith('clean_')
        ]
        # Set the loader type. If given, load data from the given location.
        self.loader = Loader()
        location = location or getattr(self, 'location', None)
        if location:
            self.load(location)
        self.error = ''

    def load(self, location):
        """
        Attempt to load data from the given location. If the data validates,
        call self.handle with that data for processing.
        """

        if hasattr(self, 'path'):
            location = os.path.join(self.path, location)
        raw_data = self.loader.load(location)
        if self.is_valid(raw_data):
            self.handle(raw_data)
        else:
            print self.error

    def is_valid(self, raw_data):
        """
        Determines if the given data is valid and returns True or False
        accordingly. If invalid, sets self.error to an error message as a
        side-effect if not set in clean_<field> and clean methods. Validation
        is performed in the following steps:

        1. Assure the data conforms to the given schema if provided
        2. Assure each field is valid using each 'clean_' method
        3. Assure all fields are valid with each other, by calling clean()
        """

        # Check the data against the asset's schema
        schema = getattr(self, 'schema', None)
        if schema:
            if not validate_data_against_schema(raw_data, schema):
                self.error = 'The given data was invalid for the schema.' + \
                    'Data was {0} but schema is {1}'.format(raw_data, schema)
                return False
        # Check each field of the data against its respective clean method
        for validator in self.field_validators:
            validator_name = validator.__name__
            field = validator_name[validator_name.find('_') + 1:]
            if not validator(raw_data.get(field, {})):
                if not self.error:
                    self.error = '{0} was not valid'.format(field)
                return False
        # Check validity of all data using clean()
        if hasattr(self, 'clean'):
            if not self.clean(raw_data):
                if not self.error:
                    self.error = '{0} did not validate'.format(raw_data)
                return False
        return True
