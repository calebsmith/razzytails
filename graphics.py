#!/usr/bin/env python
import pygame

from utils import (get_color, get_image, get_font, get_display_coordinates,
    word_wrap)
from const import GAME_STATES


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


def display_map(game_state, screen, config, level, player):
    tiles = level.map.tiles
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    tile_legend = level.map.legend
    for map_y in range(0, config.screen['map_display_height']):
        for map_x in range(0, config.screen['map_display_width']):
            display_x, display_y = get_display_coordinates(
                config, (player.x, player.y), (map_width, map_height)
            )
            current_index = level.map.get_index(
                map_x + (player.x - display_x), map_y + (player.y - display_y)
            )
            image_filename = tile_legend.get(unicode(tiles[current_index]), '')
            screen.context.blit(
                level.map.images[image_filename], (
                    map_x * config.screen['tile_width'],
                    map_y * config.screen['tile_height']
                )
            )


def display_player(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    display_x, display_y = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    draw_image(
        screen.context, config, 'razzy.png', (
            display_x * config.screen['tile_width'],
            display_y * config.screen['tile_height']
        )
    )


def display_raspberries(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset, y_offset = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    for rasp_x, rasp_y in level.map.raspberry_coordinates:
        display_x = rasp_x - (player.x - x_offset)
        display_y = rasp_y - (player.y - y_offset)
        if (display_x >= 0 and display_x < config.screen['map_display_width'] and
            display_y >= 0 and display_y < config.screen['map_display_height']):
            draw_image(
                screen.context, config, 'raspberry.png', (
                    display_x * config.screen['tile_width'],
                    display_y * config.screen['tile_height']
                )
            )


def draw_dialog(game_state, screen, config, level, player):
    # FIXME: Hard code the dialog message for now
    message = """You got a scrawburry! Nice job finding a scrawburry. There are 10 in total so there are many many scarburries out there for you. Go get some more scrawburries. You get a scrawburry, you get a scrawberry everyone gets a lorem ipsum scrawburry"""
    # Create the black surface for the dialog area to go onto
    char_width = config.dialog_box['char_width']
    char_height = config.dialog_box['char_height']
    x_margin, y_margin = 10, 10
    message_surface = pygame.Surface(
        (10 * char_width + x_margin * 2, 25 * char_height + y_margin * 2)
    )
    box_x, box_y = config.dialog_box['x'], config.dialog_box['y']
    line_offset = player.message_line_offset
    strings = word_wrap(
        message, char_width
    )[line_offset:line_offset + char_height]
    for index, string in enumerate(strings):
        draw_text(
            message_surface, config, config.score_font, string,
            (x_margin, y_margin + index * 20)
        )
        screen.context.blit(message_surface, (box_x, box_y))


def render(game_state, screen, config, level, player):
    screen.context.blit(screen.background, (0, 0))
    display_map(game_state, screen, config, level, player)
    display_raspberries(game_state, screen, config, level, player)
    display_player(game_state, screen, config, level, player)
    if game_state == GAME_STATES['dialog']:
        draw_dialog(game_state, screen, config, level, player)
    pygame.display.flip()
