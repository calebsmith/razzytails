#!/usr/bin/env python
from functools import partial
from collections import Iterable

import pygame


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
    # Dictionaries
    if hasattr(schema, 'keys'):
        for key in schema:
            if not key in data:
                return False
            if not validate_data_against_schema(data[key], schema[key]):
                return False
    # List
    elif is_non_string_iterable(schema):
        if is_non_string_iterable(data) and not hasattr(data, 'keys'):
            for value in data:
                if not validate_data_against_schema(value, schema):
                    return False
        else:
            for key in schema:
                if not validate_data_against_schema(data, key):
                    return False
    # Everything else, probably strings and numbers
    else:
        if not schema in data:
            return False
    return True


def get_color(color):
    return pygame.color.THECOLORS.get(color, None) \
        or pygame.color.THECOLORS['black']


def _get_asset(type_name, assets, filename):
    attribute = getattr(assets, type_name, None)
    return attribute.get(filename, None) if attribute else None


get_image = partial(_get_asset, 'images')
get_font = partial(_get_asset, 'fonts')
get_sounds = partial(_get_asset, 'sounds')


def _get_display_value(dimension, config, value, max_value):
    """
    Determine the display offset of the player or map tile given the current
    """
    if dimension == 'x':
        med_display_mid = config.screen['map_display_mid_x']
        max_display_value = config.screen['map_display_width']
    else:
        med_display_mid = config.screen['map_display_mid_y']
        max_display_value = config.screen['map_display_height']
    if value < med_display_mid:
        return 0
    elif value < max_value - med_display_mid:
        return value - med_display_mid
    return max_value - max_display_value

_get_display_x = partial(_get_display_value, 'x')
_get_display_y = partial(_get_display_value, 'y')


def get_display_coordinates(config, coordinates, max_coordinates):
    x, y = coordinates
    width, height = max_coordinates
    return _get_display_x(config, x, width), _get_display_y(config, y, height)


def word_wrap(sentance, limit):
    """
    A simple word wrap utility function.

    Given a sentance and a limit, return a list of strings such that no string
    is longer than the `limit`. If a single word is longer than the limit, it
    is made into two or more strings in the list, with hyphens appended at the
    end of all but the last of these strings.
    """
    results = []
    current = ''
    separator = ''
    for word in sentance.split(' '):
        if len(current) + len(word) + len(separator) <= limit:
            current += separator + word
            separator = ' '
        elif (len(word) <= limit):
            if current:
                results.append(current)
            current = word
        # Word is longer than the limit, hyphenate
        else:
            if current:
                results.append(current)
            for start in xrange(0, len(word), limit - 1):
                # If this is not the last iteration
                if start + limit - 1 < len(word):
                    results.append(word[start:start + limit - 1] + '-')
                else:
                    current = word[start:start + limit - 1]
    results.append(current)
    return results
