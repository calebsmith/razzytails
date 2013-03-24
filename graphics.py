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
            x_offset = player_x - get_display_value(player_x, map_width, 'x')
            y_offset = player_y - get_display_value(player_y, map_height, 'y')
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


def display_raspberries(assets, map_data, player):
    player_x = player['x']
    player_y = player['y']
    dimensions = map_data['map_data']['map']['dimensions']
    map_width = dimensions['width']
    map_height = dimensions['height']
    raspberry_coordinates = map_data['raspberry_coordinates']
    x_offset = player_x - get_display_value(player_x, map_width, 'x')
    y_offset = player_y - get_display_value(player_y, map_height, 'y')
    for rasp_x, rasp_y in raspberry_coordinates:
        display_x = rasp_x - x_offset
        display_y = rasp_y - y_offset
        if (display_x >= 0 and display_x <= MAP_DISPLAY_WIDTH and
            display_y >= 0 and display_y <= MAP_DISPLAY_HEIGHT):
            draw_image(
                assets['screen'], assets, 'raspberry.png',
                (display_x * TILE_WIDTH, display_y * TILE_HEIGHT)
            )


def render(assets, map_data, player):
    screen = assets['screen']
    screen.blit(assets['background'], (0, 0))
    display_map(assets, map_data, player)
    display_raspberries(assets, map_data, player)
    display_player(assets, map_data, player)
    draw_text(
        assets['screen'], assets, 'PressStart2P.ttf', 'Score:', (300, 420)
    )
    raspberries_label = 'Raspberries: {0}'.format(player['raspberries'])
    draw_text(
        assets['screen'], assets, 'PressStart2P.ttf', raspberries_label,
        (10, 420)
    )
    pygame.display.flip()
