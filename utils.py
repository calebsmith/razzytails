#!/usr/bin/env python
from functools import partial
from collections import Iterable

import pygame

from const import (MAP_DISPLAY_WIDTH, MAP_DISPLAY_HEIGHT, MAP_DISPLAY_MID_X,
    MAP_DISPLAY_MID_Y)


def is_non_string_iterable(item):
    """
    Returns True if the given item is an Iterable and is not a str, unicode,
    bytes, or bytearray; otherwise returns False.
    """
    is_iterable = isinstance(item, Iterable)
    is_string_type = isinstance(item, (str, unicode, bytes, bytearray))
    return is_iterable and not is_string_type


def validate_data_against_schema(data, schema):
    """
    Given `data`, and a `schema`, returns True if the data conforms to the
    schema provided; otherwise returns False
    """
    if hasattr(schema, 'keys'):
        for key in schema:
            if not key in data:
                return False
            if not validate_data_against_schema(data[key], schema[key]):
                return False
    elif is_non_string_iterable(schema):
        for key in schema:
            if not validate_data_against_schema(data, key):
                return False
    else:
        if not schema in data:
            return False
    return True


def get_color(color):
    return pygame.color.THECOLORS.get(color, None) \
        or pygame.color.THECOLORS['black']


def get_asset(type_name, assets, filename):
    return assets[type_name].get(filename, None)


get_image = partial(get_asset, 'images')
get_font = partial(get_asset, 'fonts')
get_sounds = partial(get_asset, 'sounds')


def get_map_index(map_width, x, y):
    return y * map_width + x


def get_display_value(value, max_value, dimension):
    """
    Determine the display offset of the player or map tile given the current
    """
    if dimension == 'x':
        med_display_mid = MAP_DISPLAY_MID_X
        max_display_value = MAP_DISPLAY_WIDTH
    else:
        med_display_mid = MAP_DISPLAY_MID_Y
        max_display_value = MAP_DISPLAY_HEIGHT
    if value < med_display_mid:
        return value
    elif value < max_value - med_display_mid:
        return med_display_mid
    return value - (max_value - max_display_value)
