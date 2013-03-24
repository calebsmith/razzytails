#!usr/bin/env python
import os
from random import shuffle
from json import loads

import pygame

from const import (SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, IMAGES_DIR,
    FONTS_DIR, SOUNDS_DIR, MAPS_DIR)
from utils import get_color, get_map_index


def initialize():
    pygame.init()
    screen = load_screen()
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(get_color('black'))
    try:
        conf_file = open(os.path.join(ASSETS_DIR, 'conf.json'))
    except IOError:
        print "No conf file found at {0}".format(ASSETS_DIR)
    conf_data = loads(conf_file.read())
    player_images = dict(map(load_image, conf_data['images']))
    fonts = dict(map(load_font, conf_data['fonts']))
    return {
        'screen': screen,
        'background': background,
        'images': player_images,
        'fonts': fonts,
    }


def load_map(map_filename):
    # Load map data
    try:
        map_data = load_map_file(map_filename)
    except IOError:
        print 'Map file {0} not found'.format(map_filename)
        return {}
    # Derive tile_solids from map data
    tiles = map_data['map']['tiles']
    dimensions = map_data['map']['dimensions']
    solids = map_data['map']['solids']
    tile_solids = [tile in solids for tile in tiles]
    # Determine coordinates with space for raspberries
    width, height = dimensions['width'], dimensions['height']
    empty_coordinates = []
    for y in xrange(height):
        for x in xrange(width):
            if not tile_solids[get_map_index(width, x, y)]:
                empty_coordinates.append((x, y))
    raspberry_coordinates = empty_coordinates
    shuffle(raspberry_coordinates)
    raspberry_coordinates = raspberry_coordinates[:10]
    # Derive image files to load from map data
    image_files = map_data['map']['legend'].values()
    images = dict(map(load_image, image_files))
    return {
        'images': images,
        'map_data': map_data,
        'tile_solids': tile_solids,
        'empty_coordinates': empty_coordinates,
        'raspberry_coordinates': raspberry_coordinates,
    }


def load_screen():
    pygame.display.set_caption("Adventure")
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def load_font(filename, font_size=16):
    font_file = os.path.join(FONTS_DIR, filename)
    try:
        font = pygame.font.Font(font_file, font_size)
    except (IOError, pygame.error):
        print 'Font file {0} not found'.format(font_file)
        font = None
    return (filename, font)


def load_image(filename):
    image_file = os.path.join(IMAGES_DIR, filename)
    try:
        image = pygame.image.load(image_file)
    except (IOError, pygame.error):
        print 'Image file {0} not found'.format(image_file)
        image = None
    return (filename, image)


def load_map_file(filename):
    map_file = os.path.join(MAPS_DIR, filename)
    f = open(map_file)
    return loads(f.read())
