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
            print "Error loading {0}".format(name)
        else:
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


class JSONManager(GenericAssetManager):

    def load(self, sub_path, name):
        if not name.endswith('.json'):
            name += '.json'
        filename = os.path.join(self.path, sub_path, name)
        f = open(filename)
        return json.loads(f.read())


class Manager(object):

    def __init__(self, asset_path):
        images_dir = os.path.join(asset_path, 'images')
        fonts_dir = os.path.join(asset_path, 'fonts')
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
