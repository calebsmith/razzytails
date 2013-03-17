#!/usr/bin/env python

import os
import sys
import time
from json import dumps, loads
from functools import partial

import pygame
from pygame.constants import *


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

MAP_DISPLAY_WIDTH = 15
MAP_DISPLAY_HEIGHT = 10
MAP_DISPLAY_MID_X = MAP_DISPLAY_WIDTH / 2
MAP_DISPLAY_MID_Y = MAP_DISPLAY_HEIGHT / 2

MAP_WIDTH = 20
MAP_HEIGHT = 12

MAP_X_DELTA = MAP_WIDTH - MAP_DISPLAY_WIDTH
MAP_Y_DELTA = MAP_HEIGHT - MAP_DISPLAY_HEIGHT

TILE_WIDTH = 32
TILE_HEIGHT = 32

PROJECT_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')

IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')


TILES = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0
]

TILE_IMAGES = {
    1: 'tree.jpg',
    0: 'grass.jpg',
}

SOLIDS = [1]

TILE_SOLIDS = [tile in SOLIDS for tile in TILES]


PLAYER_IMAGES = ('razzy-small.png',)
IMAGES = TILE_IMAGES.values()
IMAGES.extend(PLAYER_IMAGES)
FONTS = ['PressStart2P.ttf']


def initialize():
    pygame.init()
    screen = load_screen()
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(get_color('black'))
    images = dict(map(load_image, IMAGES))
    fonts = dict(map(load_font, FONTS))
    return {
        'screen': screen,
        'background': background,
        'images': images,
        'fonts': fonts,
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


def get_color(color):
    return pygame.color.THECOLORS.get(color, None) \
        or pygame.color.THECOLORS['black']


def get_asset(type_name, assets, filename):
    return assets[type_name].get(filename, None)


get_image = partial(get_asset, 'images')
get_font = partial(get_asset, 'fonts')
get_sounds = partial(get_asset, 'sounds')


def get_map_index(x, y):
    return y * MAP_WIDTH + x


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
    if image:
        surface.blit(get_image(assets, image), coordinates)


def draw_text(surface, assets, font, label, coordinates, color=None):
    if font and label:
        font = get_font(assets, font)
        text = font.render(label, True, color or get_color('white'))
        textpos = text.get_rect()
        textpos.move_ip(*coordinates)
        surface.blit(text, textpos)


def display_map(assets, player):
    player_x = player[0]
    player_y = player[1]
    for map_y in range(0, MAP_DISPLAY_HEIGHT):
        for map_x in range(0, MAP_DISPLAY_WIDTH):
            x_offset = player_x - get_display_value(player[0], MAP_WIDTH, 'x')
            y_offset = player_y - get_display_value(player[1], MAP_HEIGHT, 'y')
            current_index = get_map_index(map_x + x_offset, map_y + y_offset)
            image_filename = TILE_IMAGES.get(TILES[current_index], '')
            draw_image(
                assets['screen'], assets, image_filename,
                (map_x * TILE_WIDTH, map_y * TILE_HEIGHT)
            )


def display_player(assets, player):
    display_x = get_display_value(player[0], MAP_WIDTH, 'x')
    display_y = get_display_value(player[1], MAP_HEIGHT, 'y')
    draw_image(
        assets['screen'], assets, 'razzy-small.png',
        (display_x * TILE_WIDTH, display_y * TILE_HEIGHT)
    )


def flip(assets):
    screen = assets['screen']
    pygame.display.flip()
    screen.blit(assets['background'], (0, 0))


def render(assets, player):
    display_map(assets, player)
    display_player(assets, player)
    draw_text(assets['screen'], assets, 'PressStart2P.ttf', 'OH HAI', (400, 400))
    flip(assets)


def handle_key(event_key, player):
    current_x = player[0]
    current_y = player[1]
    if event_key == K_UP and current_y > 0:
        tile_up_index = get_map_index(current_x, current_y - 1)
        if not TILE_SOLIDS[tile_up_index]:
            player[1] -= 1
    if event_key == K_DOWN and current_y < MAP_HEIGHT - 1:
        tile_down_index = get_map_index(current_x, current_y + 1)
        if not TILE_SOLIDS[tile_down_index]:
            player[1] += 1
    if event_key == K_LEFT and current_x > 0:
        tile_left_index = get_map_index(current_x - 1, current_y)
        if not TILE_SOLIDS[tile_left_index]:
            player[0] -= 1
    if event_key == K_RIGHT and current_x < MAP_WIDTH - 1:
        tile_right_index = get_map_index(current_x + 1, current_y)
        if not TILE_SOLIDS[tile_right_index]:
            player[0] += 1


def main(*args):
    # Initialize display screen and load assets
    assets = initialize()
    player = [0, 0]
    while True:
        # Exit on escape key or X
        for event in pygame.event.get():
            pressed_escape = event.type == KEYUP and event.key == K_ESCAPE
            if pressed_escape or event.type == QUIT:
                return
            if event.type == KEYDOWN:
                handle_key(event.key, player)
        time.sleep(0.05)
        render(assets, player)


if __name__ == "__main__":
    main(sys.argv)
