import os

import pygame
from pygame import display, Surface

from const import MAPS_DIR, CONFIG_DIR, FONTS_DIR, IMAGES_DIR
from asset_loaders import Asset, LoadableAsset
from utils import get_color


class Screen(Asset):

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self._create_context()

    def _create_context(self):
        display.set_caption(self.title)
        self.context = display.set_mode((self.width, self.height))

    def handle(self, data):
        super(Screen, self).handle(data)
        self.map_display_mid_x = self.map_display_width / 2
        self.map_display_mid_y = self.map_display_height / 2

    def set_background(self, color):
        background = Surface(self.context.get_size()).convert()
        background.fill(get_color(color))
        self.background = background


class Map(Asset):
    pass


class Items(Asset):
    pass


class Mobs(Asset):
    pass


class Level(LoadableAsset):

    path = MAPS_DIR
    schema = {
        'map': [
            'solids',
            'legend',
            'tiles',
            {
                'dimensions': [
                    'width', 'height'
                ],
            },
        ],
        'player_start': [
            'x', 'y'
        ],
    }

    def clean_map(self, map_data):
        dimensions = map_data['dimensions']
        num_tiles = dimensions['width'] * dimensions['height']
        if len(map_data['tiles']) != num_tiles:
            self.error = u'Number of tiles must equal width * height'
            return False
        return True

    def clean(self, raw_data):
        player_start = raw_data['player_start']
        dimensions = raw_data['map']['dimensions']
        x, y = player_start['x'], player_start['y']
        if x < 0 or y < 0 or x >= dimensions['width'] or y >= dimensions['height']:
            self.error = u'The player_start x or y is out of bounds'
            return False
        return True

    def handle(self, data):
        self.map = Map(data['map'])
        self.player_start = data['player_start']


class Config(LoadableAsset):

    path = CONFIG_DIR
    location = 'config.json'
    schema = [{
        'screen': [
            'title',
            'width',
            'height',
            'tile_width',
            'tile_height',
            'map_display_width',
            'map_display_height',
        ]},
        'images',
        'fonts'
    ]

    def handle(self, data):
        super(Config, self).handle(data)
        self.images = dict(map(self.load_image, self.images))
        self.fonts = dict(map(self.load_font, self.fonts))

    def load_font(self, filename, font_size=16):
        font_file = os.path.join(FONTS_DIR, filename)
        try:
            font = pygame.font.Font(font_file, font_size)
        except (IOError, pygame.error):
            print 'Font file {0} not found'.format(font_file)
            font = None
        return (filename, font)

    def load_image(self, filename):
        image_file = os.path.join(IMAGES_DIR, filename)
        try:
            image = pygame.image.load(image_file)
        except (IOError, pygame.error):
            print 'Image file {0} not found'.format(image_file)
            image = None
        return (filename, image)
