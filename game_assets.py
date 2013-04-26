import os
from random import randrange

from pygame import display, Surface

from const import MAPS_DIR, CONFIG_DIR, MUSIC_DIR
from asset_loaders import Asset, LoadableAsset, load_image, load_font
from utils import get_color


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
        'start',
        'images',
        'fonts',
        'music',
        'score_font',
        'raspberries_font', {
            'dialog_box': [
                'x', 'y', 'char_width', 'char_height'
            ]
        },
        {'keypress_repeat': [
            'delay',
            'interval'
            ]
        }
    ]

    def handle(self, data):
        super(Config, self).handle(data)
        self.images = dict(map(load_image, self.images))
        self.fonts = dict(map(load_font, self.fonts))
        self.music = os.path.join(MUSIC_DIR, self.music) if self.music else ''
        self.screen['map_display_mid_x'] = self.screen['map_display_width'] / 2
        self.screen['map_display_mid_y'] = self.screen['map_display_height'] / 2


class Screen(Asset):

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self._create_context()

    def _create_context(self):
        display.set_caption(self.title)
        self.context = display.set_mode((self.width, self.height))

    def set_background(self, color=''):
        color = color or 'black'
        background = Surface(self.context.get_size()).convert()
        background.fill(get_color(color))
        self.background = background


class Map(Asset):

    def handle(self, data):
        super(Map, self).handle(data)
        self.tile_solids = [tile in self.solids for tile in self.tiles]
        self.images = dict(map(load_image, self.legend.values()))

    def get_index(self, x, y):
        return y * self.dimensions['width'] + x


class Item(Asset):
    pass


class Monster(Asset):
    x = 0
    y = 0

    def handle(self, data):
        super(Monster, self).handle(data)
        self.image = load_image(self.image)


class Player(Asset):
    x = 0
    y = 0
    raspberries = 0
    message_line_offset = 0
    items = []


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
            {
                'player_start': [
                    'x', 'y'
                ],
            }
        ],
        'monsters': [
            'image',
            'number'
        ]
    }

    def clean_map(self, map_data):
        player_start = map_data['player_start']
        x, y = player_start['x'], player_start['y']
        dimensions = map_data['dimensions']
        num_tiles = dimensions['width'] * dimensions['height']
        if len(map_data['tiles']) != num_tiles:
            self.error = u'Number of tiles must equal width * height'
            return False
        if x < 0 or y < 0 or x >= dimensions['width'] or y >= dimensions['height']:
            self.error = u'The player_start x or y is out of bounds'
            return False
        return True

    def clean_monsters(self, monster_data):
        num_monsters = monster_data['number']
        if num_monsters < 1:
            self.error = u'You need at least 1 monster'
            return False
        return True

    def handle(self, data):
        self.map = Map(data['map'])
        self.monsters = []

        for i in range(data['monsters']['number']):
            monster = Monster(data['monsters'])
            self._place_monster(monster, self.map)
            self.monsters.append(monster)

    def _place_monster(self, monster, map):
        found_spot = False
        while found_spot is False:
            # Pick a random spot on the map
            x = randrange(map.dimensions['width'])
            y = randrange(map.dimensions['height'])
            # map.tile_solids will be false if spot is not yet taken
            found_spot = not map.tile_solids[map.get_index(x, y)]
            if (x, y) == (map.player_start['x'], map.player_start['y']):
                found_spot = False # don't start on top of player
        monster.x, monster.y = x, y
