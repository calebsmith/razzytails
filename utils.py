#!/usr/bin/env python
from functools import partial

import pygame

from const import (MAP_DISPLAY_WIDTH, MAP_DISPLAY_HEIGHT, MAP_DISPLAY_MID_X,
    MAP_DISPLAY_MID_Y)


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
