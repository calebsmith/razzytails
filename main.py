#!/usr/bin/env python

import os
import sys
import time
from json import loads
from functools import partial

import pygame
from pygame.constants import (KEYUP, KEYDOWN, K_ESCAPE, QUIT, K_UP, K_DOWN,
    K_LEFT, K_RIGHT)

from const import (SCREEN_WIDTH, SCREEN_HEIGHT, MAP_DISPLAY_WIDTH,
    MAP_DISPLAY_HEIGHT, MAP_DISPLAY_MID_X, MAP_DISPLAY_MID_Y, TILE_WIDTH,
    TILE_HEIGHT, ASSETS_DIR, IMAGES_DIR, FONTS_DIR, SOUNDS_DIR, MAPS_DIR)


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
    map_data = load_map_file(map_filename)
    # Derive tile_solids from map data
    tiles = map_data['map']['tiles']
    solids = map_data['map']['solids']
    tile_solids = [tile in solids for tile in tiles]
    # Derive image files to load from map data and also load player images
    image_files = map_data['map']['legend'].values()
    images = dict(map(load_image, image_files))
    return {
        'images': images,
        'map_data': map_data,
        'tile_solids': tile_solids,
    }


def load_screen():
    pygame.display.set_caption("Adventure")
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def load_font(filename, font_size=16):
    font_file = os.path.join(FONTS_DIR, filename)
    return (filename, pygame.font.Font(font_file, font_size))


def load_image(filename):
    image_file = os.path.join(IMAGES_DIR, filename)
    return (filename, pygame.image.load(image_file))


def load_map_file(filename):
    map_file = os.path.join(MAPS_DIR, filename)
    f = open(map_file)
    return loads(f.read())


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


def draw_image(surface, assets, image, coordinates):
    if image and surface:
        surface.blit(get_image(assets, image), coordinates)


def draw_text(surface, assets, font, label, coordinates, color=None):
    if all((surface, font, label)):
        font = get_font(assets, font)
        text = font.render(label, True, color or get_color('white'))
        textpos = text.get_rect()
        textpos.move_ip(*coordinates)
        surface.blit(text, textpos)


def display_map(assets, map_data, player):
    player_x = player['x']
    player_y = player['y']
    tiles = map_data['map_data']['map']['tiles']
    dimensions = map_data['map_data']['map']['dimensions']
    map_width = dimensions['width']
    map_height = dimensions['height']
    tile_legend = map_data['map_data']['map']['legend']
    for map_y in range(0, MAP_DISPLAY_HEIGHT):
        for map_x in range(0, MAP_DISPLAY_WIDTH):
            x_offset = player_x - get_display_value(player['x'], map_width, 'x')
            y_offset = player_y - get_display_value(player['y'], map_height, 'y')
            current_index = get_map_index(
                map_width, map_x + x_offset, map_y + y_offset
            )
            image_filename = tile_legend.get(unicode(tiles[current_index]), '')
            draw_image(
                assets['screen'], map_data, image_filename,
                (map_x * TILE_WIDTH, map_y * TILE_HEIGHT)
            )


def display_player(assets, map_data, player):
    dimensions = map_data['map_data']['map']['dimensions']
    map_width = dimensions['width']
    map_height = dimensions['height']
    display_x = get_display_value(player['x'], map_width, 'x')
    display_y = get_display_value(player['y'], map_height, 'y')
    draw_image(
        assets['screen'], assets, 'razzy-small.png',
        (display_x * TILE_WIDTH, display_y * TILE_HEIGHT)
    )


def flip(assets):
    screen = assets['screen']
    pygame.display.flip()
    screen.blit(assets['background'], (0, 0))


def render(assets, map_data, player):
    display_map(assets, map_data, player)
    display_player(assets, map_data, player)
    draw_text(assets['screen'], assets, 'PressStart2P.ttf', 'OH HAI', (400, 400))
    flip(assets)


def handle_key(event_key, map_data, player):
    current_x = player['x']
    current_y = player['y']
    dimensions = map_data['map_data']['map']['dimensions']
    map_width = dimensions['width']
    map_height = dimensions['height']
    tile_solids = map_data['tile_solids']
    if event_key == K_UP and current_y > 0:
        tile_up_index = get_map_index(map_width, current_x, current_y - 1)
        if not tile_solids[tile_up_index]:
            player['y'] -= 1
    if event_key == K_DOWN and current_y < map_height - 1:
        tile_down_index = get_map_index(map_width, current_x, current_y + 1)
        if not tile_solids[tile_down_index]:
            player['y'] += 1
    if event_key == K_LEFT and current_x > 0:
        tile_left_index = get_map_index(map_width, current_x - 1, current_y)
        if not tile_solids[tile_left_index]:
            player['x'] -= 1
    if event_key == K_RIGHT and current_x < map_width - 1:
        tile_right_index = get_map_index(map_width, current_x + 1, current_y)
        if not tile_solids[tile_right_index]:
            player['x'] += 1


def main(*args):
    # Initialize display screen and load assets
    assets = initialize()
    map_data = load_map('map1.json')
    player = map_data['map_data']['player_start']
    while True:
        # Exit on escape key or X
        for event in pygame.event.get():
            pressed_escape = event.type == KEYUP and event.key == K_ESCAPE
            if pressed_escape or event.type == QUIT:
                return
            if event.type == KEYDOWN:
                handle_key(event.key, map_data, player)
        time.sleep(0.05)
        render(assets, map_data, player)


if __name__ == "__main__":
    main(sys.argv)
