#!/usr/bin/env python

import os
import sys
import time
from functools import partial

import pygame
from pygame.constants import *


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

MAP_WIDTH = 15
MAP_HEIGHT = 10

TILE_WIDTH = 32
TILE_HEIGHT = 32

PROJECT_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')

IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

TILES = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

TILE_IMAGES = {
    1: 'tree.jpg',
    0: 'grass.jpg',
}

PLAYER_IMAGES = ('razzy-small.png',)

SOLIDS = [1]

TILE_SOLIDS = [tile in SOLIDS for tile in TILES]

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


def draw_image(surface, assets, image, coordinates):
    if image:
        surface.blit(get_image(assets, image), coordinates)


def draw_text(surface, assets, font, label, coordinates, color=None):
    font = get_font(assets, font)
    text = font.render(label, True, color or get_color('white'))
    textpos = text.get_rect()
    textpos.move_ip(*coordinates)
    surface.blit(text, textpos)


def display_map(assets):
    for index, tile in enumerate(TILES):
        x = (index % MAP_WIDTH)
        y = index / MAP_WIDTH
        image_filename = TILE_IMAGES.get(tile, '')
        draw_image(
            assets['screen'], assets, image_filename,
            (x * TILE_WIDTH, y * TILE_HEIGHT)
        )


def display_player(assets, player):
    x = player[0] * TILE_WIDTH
    y = player[1] * TILE_HEIGHT
    draw_image(assets['screen'], assets, 'razzy-small.png', (x, y))


def flip(assets):
    screen = assets['screen']
    pygame.display.flip()
    screen.blit(assets['background'], (0, 0))


def render(assets, player):
    display_map(assets)
    display_player(assets, player)
    draw_text(assets['screen'], assets, 'PressStart2P.ttf', 'OH HAI', (400, 400))
    flip(assets)


def handle_key(event_key, player):
    current_x = player[0]
    current_y = player[1]
    if event_key == K_UP:
        tile_up_index = get_map_index(current_x, current_y - 1)
        if not TILE_SOLIDS[tile_up_index]:
            player[1] -= 1
    if event_key == K_DOWN:
        tile_down_index = get_map_index(current_x, current_y + 1)
        if not TILE_SOLIDS[tile_down_index]:
            player[1] += 1
    if event_key == K_LEFT:
        tile_left_index = get_map_index(current_x - 1, current_y)
        if not TILE_SOLIDS[tile_left_index]:
            player[0] -= 1
    if event_key == K_RIGHT:
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
