#!usr/bin/env python
import os
from random import shuffle
from json import loads

import pygame

from const import (SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, IMAGES_DIR,
    FONTS_DIR, SOUNDS_DIR, MAPS_DIR)
from utils import get_map_index

from game_assets import Config, Level, Screen


def initialize():
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a two tuple in the form of: (config, screen)
    """
    pygame.init()
    config = Config()
    screen = Screen(config.screen)
    screen.set_background('black')
    return config, screen


def load_map(map_filename):
    level = Level(map_filename)
    # TODO: Remove once items are added
    # Create and attach raspberry coordinates.
    width, height = level.map.dimensions['width'], level.map.dimensions['height']
    raspberry_coordinates = []
    for y in xrange(height):
        for x in xrange(width):
            if not level.map.tile_solids[get_map_index(width, x, y)]:
                raspberry_coordinates.append((x, y))
    shuffle(raspberry_coordinates)
    level.map.raspberry_coordinates = raspberry_coordinates[:10]
    return level
