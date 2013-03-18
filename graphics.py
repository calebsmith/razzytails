#!/usr/bin/env python
import pygame

from const import (SCREEN_WIDTH, SCREEN_HEIGHT, MAP_DISPLAY_WIDTH,
    MAP_DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
from utils import (get_color, get_image, get_font, get_display_value,
    get_map_index)


def draw_image(surface, assets, image_name, coordinates):
    image = get_image(assets, image_name)
    if image and surface:
        surface.blit(image, coordinates)


def draw_text(surface, assets, font_name, label, coordinates, color=None):
    font = get_font(assets, font_name)
    if all((surface, font, label)):
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
            x_offset = player_x - get_display_value(
                player['x'], map_width, 'x'
            )
            y_offset = player_y - get_display_value(
                player['y'], map_height, 'y'
            )
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
    draw_text(
        assets['screen'], assets, 'PressStart2P.ttf', 'Hello', (400, 400)
    )
    flip(assets)
