import os
import json

from yape.utils import validate_data_against_schema


class BaseComponent(object):
    """
    A base class that defines methods common to the Component and
    LoadableComponent classes.
    """

    field_method_mapping = [
        ('image_fields', 'get_image'),
        ('sprite_fields', 'get_sprite'),
        ('font_fields', 'get_font'),
        ('json_fields', 'get_json'),
    ]

    def __init__(self, manager, *args):
        self.manager = manager
        # Determine what methods to call when validating individual fields
        self.field_validators = [
            getattr(self, attr)
            for attr in dir(self)
            if attr.startswith('clean_')
        ]
        self.error = ''

    def load(self, data):
        if self.is_valid(data):
            self.process_data(data)
            self.process_auto_fields()
            if hasattr(self, 'post_process'):
                self.post_process()
        else:
            print self.error

    def process_data(self, data):
        """
        Handle data once it has been validated. By default, assigns values from
        data to attributes on self if data is a dictionary.
        """
        if hasattr(data, 'items'):
            for key, value in data.items():
                setattr(self, key, value)

    def process_auto_fields(self):
        """
        Replaces image, font, sound, and json fields with references to those
        objects, using the component's manager. Uses the component's *_fields
        methods to determine what fields should be associated with a given type
        of asset (such as image, or font).
        """
        for field_type, manager_method in self.field_method_mapping:
            asset_field_names = getattr(self, field_type, [])
            for asset_field_name in asset_field_names:
                asset_args = getattr(self, asset_field_name, None)
                if asset_args is not None:
                    # If the field is a dictionary, load assets for its values and
                    # assign them to the keys of the dictionary
                    if isinstance(asset_args, dict):
                        for key, value in asset_args.items():
                            asset_ref = self._get_asset_ref(field_type, manager_method, asset_field_name, value)
                            asset_args[key] = asset_ref
                    else:
                        asset_ref = self._get_asset_ref(field_type, manager_method, asset_field_name, asset_args)
                        setattr(self, asset_field_name, asset_ref)

    def _get_asset_ref(self, field_type, manager_method, asset_field_name, asset_args):
        """
        Uses manager methods to load assets on behalf of a field in a *_fields
        declaration.
        """
        # image field values are filenames only, while other asset
        # arguments are iterable. Wrap filename inside a list so it
        # dereferences properly when load_func is called
        if field_type == 'image_fields':
            asset_args = [asset_args]
        # sprite field values specify an x and y offset, but not a
        # width height. These are defined on the asset class itself
        if field_type == 'sprite_fields':
            width, height = self.sprite_fields[asset_field_name]
            asset_args = list(asset_args)
            asset_args.extend([width, height])
        # Determine what method to call on the manager for the
        # current field type
        load_func = getattr(self.manager, manager_method)
        asset = load_func(*asset_args)
        if asset is None:
            err_msg = 'Failed to load {0} for {1} attribute in {2}'
            print err_msg.format(
                asset_args, asset_field_name, self.__class__.__name__
            )
        return asset

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

        # Check the data against the component's schema
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


class Component(BaseComponent):
    """
    A game component that is instantiated with data and does not load it directly.
    """

    def __init__(self, manager, data=None):
        super(Component, self).__init__(manager)
        if data is not None:
            self.raw_data = data
            self.load(data)


class LoadableComponent(BaseComponent):
    """
    A game component or container of components that is instatiated with a location,
    and loads data from that location to fill itself with components and assets.
    """

    def __init__(self, manager, location=None):
        super(LoadableComponent, self).__init__(manager)
        location = location or getattr(self, 'location', None)
        if location:
            self.load_location(location)
            self.load(self.raw_data)

    def load_location(self, location):
        """
        Attempt to load data from the given location.
        """
        path = getattr(self, 'path', '')
        self.raw_data = self.manager.get_json(path, location)

