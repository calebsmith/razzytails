#!/usr/bin/env python
import pygame

from const import (SCREEN_WIDTH, SCREEN_HEIGHT, MAP_DISPLAY_WIDTH,
    MAP_DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
from utils import (get_color, get_image, get_font, get_display_value,
    get_map_index)


def draw_image(surface, obj, image_name, coordinates):
    image = get_image(obj, image_name)
    if image and surface:
        surface.blit(image, coordinates)


def draw_text(surface, obj, font_name, label, coordinates, color=None):
    font = get_font(obj, font_name)
    if all((surface, font, label)):
        text = font.render(label, True, color or get_color('white'))
        textpos = text.get_rect()
        textpos.move_ip(*coordinates)
        surface.blit(text, textpos)


def display_map(screen, config, level, player):
    player_x = player['x']
    player_y = player['y']
    tiles = level.map.tiles
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    tile_legend = level.map.legend
    for map_y in range(0, MAP_DISPLAY_HEIGHT):
        for map_x in range(0, MAP_DISPLAY_WIDTH):
            x_offset = player_x - get_display_value(player_x, map_width, 'x')
            y_offset = player_y - get_display_value(player_y, map_height, 'y')
            current_index = get_map_index(
                map_width, map_x + x_offset, map_y + y_offset
            )
            image_filename = tile_legend.get(unicode(tiles[current_index]), '')
            screen.context.blit(
                level.map.images[image_filename],
                (map_x * TILE_WIDTH, map_y * TILE_HEIGHT)
            )


def display_player(screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    display_x = get_display_value(player['x'], map_width, 'x')
    display_y = get_display_value(player['y'], map_height, 'y')
    draw_image(
        screen.context, config, 'razzy-small.png',
        (display_x * TILE_WIDTH, display_y * TILE_HEIGHT)
    )


def display_raspberries(screen, config, level, player):
    player_x = player['x']
    player_y = player['y']
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset = player_x - get_display_value(player_x, map_width, 'x')
    y_offset = player_y - get_display_value(player_y, map_height, 'y')
    for rasp_x, rasp_y in level.map.raspberry_coordinates:
        display_x = rasp_x - x_offset
        display_y = rasp_y - y_offset
        if (display_x >= 0 and display_x < MAP_DISPLAY_WIDTH and
            display_y >= 0 and display_y < MAP_DISPLAY_HEIGHT):
            draw_image(
                screen.context, config, 'raspberry.png',
                (display_x * TILE_WIDTH, display_y * TILE_HEIGHT)
            )


def render(screen, config, level, player):
    screen.context.blit(screen.background, (0, 0))
    display_map(screen, config, level, player)
    display_raspberries(screen, config, level, player)
    display_player(screen, config, level, player)
    draw_text(
        screen.context, config, 'PressStart2P.ttf', 'Score:', (300, 420)
    )
    raspberries_label = 'Raspberries: {0}'.format(player['raspberries'])
    draw_text(
        screen.context, config, 'PressStart2P.ttf', raspberries_label,
        (10, 420)
    )
    pygame.display.flip()
