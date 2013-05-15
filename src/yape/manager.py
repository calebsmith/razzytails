import os
import json
from weakref import WeakValueDictionary

import pygame


class GenericAssetManager(object):

    def __init__(self, path):
        self.path = path
        self.cache = WeakValueDictionary()

    def _load_asset(self, *args):
        try:
            asset = self.load(*args)
        except (IOError, pygame.error):
            asset = None
            print "Error loading {0}".format(args)
        else:
            if asset is not None:
                self.cache[args] = asset
        return asset

    def get(self, *args):
        try:
            asset = self.cache[args]
        except KeyError:
            asset = self._load_asset(*args)
        return asset


class ImageManager(GenericAssetManager):

    def load(self, name):
        filename = os.path.join(self.path, name)
        return pygame.image.load(filename).convert_alpha()


class FontManager(GenericAssetManager):

    def load(self, name, font_size):
        filename = os.path.join(self.path, name)
        return pygame.font.Font(filename, font_size)


class JSONDict(dict):
    """A dictionary for storing JSON data that can be weak referenced"""

    def __init__(self, json_data):
        self.update(json_data)


class JSONList(list):
    """A list for storing JSON data that can be weak referenced"""

    def __init__(self, json_data):
        self.extend(json_data)


class JSONManager(GenericAssetManager):

    def load(self, sub_path, name):
        filename = os.path.join(self.path, sub_path, name)
        f = open(filename)
        try:
            json_data = json.loads(f.read())
        except ValueError as e:
            print 'Invalid JSON in file {0}. {1}'.format(filename, e)
            return None
        kls = JSONDict if isinstance(json_data, dict) else JSONList
        return kls(json_data)


class Manager(object):
    """
    Client class for obtaining and cacheing unique references to assets from
    the filesystem. Uses weak references to hold a unique object in memory
    while used and free it once it is no longer in use.
    """

    def __init__(self, assets_dir):
        images_dir = os.path.join(assets_dir, 'images')
        fonts_dir = os.path.join(assets_dir, 'fonts')
        self.json_manager = JSONManager(assets_dir)
        self.image_manager = ImageManager(images_dir)
        self.font_manager = FontManager(fonts_dir)

    def _get_asset(self, manager, *args):
        return manager.get(*args)

    def get_json(self, sub_path, filename):
        return self._get_asset(self.json_manager, sub_path, filename)

    def get_image(self, filename):
        return self._get_asset(self.image_manager, filename)

    def get_font(self, filename, font_size):
        return self._get_asset(self.font_manager, filename, font_size)

