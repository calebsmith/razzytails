import os
import json

from const import MAPS_DIR


class InvalidSchema(Exception):
    pass


class InvalidValue(Exception):
    pass


def validate_data_against_schema(data, schema):
    if hasattr(schema, 'keys'):
        for key in schema.keys():
            if not key in data:
                return False
    else:
        for value in schema:
            if hasattr(value, 'keys'):
                for key, sub_value in value.items():
                    if not validate_data_against_schema(data[key], sub_value):
                        return False
            else:
                if not value in data:
                    return False
    if hasattr(schema, 'keys'):
        for key in schema.keys():
            if not validate_data_against_schema(data[key], schema[key]):
                return False
    return True


class Loader(object):

    def load(self, location):
        contents = self.load_contents(location)
        return self.coerce_contents(contents)

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

    def load_contents(self, filename):
        """Load data from the local file system"""
        try:
            level_file = os.path.join(MAPS_DIR, filename)
            return open(level_file).read()
        except IOError:
            return None

    def coerce_contents(self, contents):
        """Parse the file as JSON"""
        return json.loads(contents)


class RootAsset(object):

    def __init__(self, location=None, Loader=JSONFileLoader):
        self.field_validators = [
            getattr(self, attr)
            for attr in dir(self)
            if attr.startswith('clean_')
        ]
        if hasattr(self, 'clean'):
            self.field_validators.append(self.clean)

        self.loader = Loader()
        if location:
            self.load(location)

    def load(self, filename):
        raw_data = self.loader.load(filename)
        if self.is_valid(raw_data):
            self.handle(raw_data)

    def is_valid(self, raw_data):
        schema = getattr(self, 'schema', None)
        if schema:
            if not self.validate_schema(raw_data, schema):
                return False
        for validator in self.field_validators:
            validator_name = validator.__name__
            if '_' not in validator_name:
                valid = validator(raw_data)
            else:
                field = validator_name[validator_name.index('_') + 1:]
                valid = validator(raw_data.get(field, {}))
            if not valid:
                return False
        return True

    def validate_schema(self, raw_data, schema):
        return validate_data_against_schema(raw_data, schema)

    def handle(self, data):
        self.assign_to_self(data)


class Asset(object):

    def __init__(self, data=None):
        if data:
            self.assign_to_self(data)

    def assign_to_self(self, data):
        self.data = data
        for key, value in data.items():
            setattr(self, key, value)
        self.post_process()

    def post_process(self):
        pass


class Map(Asset):
    pass


class Items(Asset):
    pass


class Mobs(Asset):
    pass


class Level(RootAsset):

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
