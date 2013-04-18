from const import MAPS_DIR
from asset_loaders import Asset, LoadableAsset


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
