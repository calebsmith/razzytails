from copy import copy
import os
import random

from const import MAPS_DIR, CONFIG_DIR, MUSIC_DIR
from asset_loaders import Asset, LoadableAsset, load_image, load_font
from yape.utils import word_wrap


class Config(LoadableAsset):

    path = CONFIG_DIR
    location = 'config.json'
    schema = [
        'start',
        'images',
        'player_image',
        'splash_image',
        'endscreen_image',
        'fonts',
        'score_font',
        'music', {
            'popup_box': [
                'x', 'y', 'char_width', 'char_height'
            ]
        },
        {
            'keypress_repeat': [
                'delay',
                'interval'
            ]
        },
        'questions',
        'monster_delay',
        {
            'joystick': [
                'delay',
                'pressed'
            ]
        }
    ]

    def handle(self, data):
        super(Config, self).handle(data)
        self.questions = Questions(
            self.questions, width=self.popup_box['char_width']
        )
        self.data = data

    def load_assets(self):
        """
        Load the asset files whose names are set in the config file.

        N.B. This is done in a separate step than handle() because the screen
        context must be set before images are loaded, but the screen context
        uses config data for determining the width and height of the video mode
        """
        images, fonts, music = self.data['images'], self.data['fonts'], self.data['music']
        self.images = dict(map(load_image, images))
        self.fonts = dict(map(load_font, fonts))
        self.music = os.path.join(MUSIC_DIR, music) if self.music else ''


class Questions(LoadableAsset):
    path = CONFIG_DIR
    schema = [
        'question',
        'answers',
        'correct',
    ]

    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', 20)
        super(Questions, self).__init__(*args, **kwargs)
        self.next()

    def next(self):
        self.current_index = random.choice(range(len(self.questions)))
        self.current_question = self.questions[self.current_index]
        self.choice = 0
        self._question_display = None

    def handle(self, data):
        self.questions = data
        self.question_displays = [
            word_wrap(question['question'], self.width)
            for question in self.questions
        ]

    def get_choices_length(self):
        return len(self.current_question['answers'])

    def get_question_display(self):
        question_display = copy(self.question_displays[self.current_index])
        question_display.append('')
        for index, answer in enumerate(self.current_question['answers']):
            prefix = '[X] ' if index == self.choice else '[ ] '
            question_display.extend(word_wrap(prefix + answer, self.width))
        return question_display

    def is_correct(self):
        return self.choice == self.current_question['correct']


class Map(Asset):

    def handle(self, data):
        super(Map, self).handle(data)
        self.tile_solids = [tile in self.solids for tile in self.tiles]
        self.images = dict(map(load_image, self.legend.values()))

    def get_index(self, x, y):
        return y * self.dimensions['width'] + x


class Item(Asset):

    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', 20)
        super(Item, self).__init__(*args, **kwargs)

    def handle(self, data):
        super(Item, self).handle(data)
        self.message = word_wrap(self.message, self.width) + ['', 'Press "Enter" to continue']


class Monster(Asset):
    x = 0
    y = 0
    last_moved_at = 0

    def place_on_map(self, map_data):
        found_spot = False
        while found_spot is False:
            # Pick a random spot on the map
            x = random.randrange(map_data.dimensions['width'])
            y = random.randrange(map_data.dimensions['height'])
            # map.tile_solids will be false if spot is not yet taken
            found_spot = not map_data.tile_solids[map_data.get_index(x, y)]
            if (x, y) == (map_data.player_start['x'], map_data.player_start['y']):
                # don't start on top of player
                found_spot = False
        self.x, self.y = x, y

    def move(self, level, player):
        """Move the monster.

        Needs 'level' so we can make sure not to step on solids. Needs
        'player' so we can aim for the player.
        """
        map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
        tile_solids = level.map.tile_solids
        mc = level.monster_coordinates
        # Remove self from monster_coordinates
        del mc[self.id]

        all_possible_moves = [(self.x + 1, self.y),
                              (self.x - 1, self.y),
                              (self.x, self.y),
                              (self.x, self.y - 1),
                              (self.x, self.y + 1)]
        free_moves = []
        for x, y in all_possible_moves:
            # on the map?
            if x >= 0 and y >= 0 and x < map_width and y < map_height:
                # not on a solid?
                if not tile_solids[level.map.get_index(x, y)]:
                    # not on another monster?
                    if (x, y) not in mc.values():
                        free_moves.append((x, y))

        min_distance = len(tile_solids) + 1  # start with big number
        best_move = (-1, -1)
        for move in free_moves:
            distance = self._distance_from_player(move, player)
            if distance < min_distance:
                min_distance = distance
                best_move = move
        self.x, self.y = best_move
        mc.update({self.id: best_move})

    def _distance_from_player(self, position, player):
        """Return a crude distance calculation between 2 positions.

        This is simply the sum of the absolute value of x and y distances"""
        move_x, move_y = position
        return abs(move_x - player.x) + abs(move_y - player.y)


class Player(Asset):
    x = 0
    y = 0
    items = []
    last_updated = None
    neutral = True

    # Some directions constants for general use.
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    # Maps a direction constant to a two-tuple, the first of which is the
    # intended change of x and y in the form of (x, y). The second value is
    # the predicate function that determines if the move is within bounds
    _direction_mapping = {
        UP: ((0, -1), lambda x, y, x_bounds, y_bounds: y > 0),
        DOWN: ((0, 1), lambda x, y, x_bounds, y_bounds: y < y_bounds),
        LEFT: ((-1, 0), lambda x, y, x_bounds, y_bounds: x > 0),
        RIGHT: ((1, 0), lambda x, y, x_bounds, y_bounds: x < x_bounds),
    }

    def _move(self, level, direction):
        dimensions = level.map.dimensions
        map_width, map_height = dimensions['width'], dimensions['height']
        (x_modifier, y_modifier), bounds_func = self._direction_mapping[direction]
        inbounds = bounds_func(self.x, self.y, map_width - 1, map_height - 1)
        if not inbounds:
            return
        tile_solids = level.map.tile_solids
        goal_tile_index = level.map.get_index(
            self.x + x_modifier, self.y + y_modifier
        )
        if not tile_solids[goal_tile_index]:
            self.x += x_modifier
            self.y += y_modifier

    def move_up(self, level):
        self._move(level, self.UP)

    def move_down(self, level):
        self._move(level, self.DOWN)

    def move_left(self, level):
        self._move(level, self.LEFT)

    def move_right(self, level):
        self._move(level, self.RIGHT)


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
        ],
        'items': [
            'id',
            'title',
            'image',
            'message'
        ]
    }

    def __init__(self, config):
        self.config = config
        super(Level, self).__init__(config.start)

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
        self.monster_data = data['monsters']
        self.reset_monsters()

        self.item_coordinates = []
        self.items = []
        item_locations = self._generate_item_locations(self.map)
        for index, item_data in enumerate(data['items']):
            location = item_locations[index]
            item = Item(item_data, width=self.config.popup_box['char_width'])
            self.items.append(item)
            self.item_coordinates.append({
                'id': item.id, 'coordinates': location
            })
        # Load and store image files for monster and item objects
        monster_images = dict([
            load_image(monster.image)
            for monster in self.monsters
        ])
        item_images = dict([
            load_image(item.image)
            for item in self.items
        ])
        self.images = monster_images
        self.images.update(item_images)

    def reset_items(self, player):
        self.item_coordinates = []
        player.items = []
        item_locations = self._generate_item_locations(self.map)
        for index, item in enumerate(self.items):
            location = item_locations[index]
            self.item_coordinates.append({
                'id': item.id, 'coordinates': location
            })

    def _generate_item_locations(self, map_data):
        locations = []
        width, height = map_data.dimensions['width'], map_data.dimensions['height']
        for y in xrange(height):
            for x in xrange(width):
                if not map_data.tile_solids[map_data.get_index(x, y)]:
                    locations.append((x, y))
        random.shuffle(locations)
        return locations

    def reset_monsters(self):
        self.monsters = []
        self.monster_coordinates = {}
        for i in range(self.monster_data['number']):
            self.monster_data.update({'id': i})
            monster = Monster(self.monster_data)
            monster.place_on_map(self.map)
            self.monsters.append(monster)
            self.monster_coordinates[i] = (monster.x, monster.y)
