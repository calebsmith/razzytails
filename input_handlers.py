#!/usr/bin/env python
import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_SPACE
from pygame.constants import KEYDOWN, K_ESCAPE, QUIT

from const import GAME_STATES


def handle_events(game_state, config, level, player):
    for event in pygame.event.get():
        # Exit on escape key or clicking X
        pressed_escape = event.type == KEYDOWN and event.key == K_ESCAPE
        if pressed_escape or event.type == QUIT:
            return GAME_STATES['exit']
        if event.type == KEYDOWN and game_state == GAME_STATES['dialog']:
            game_state = handle_dialog(game_state, config, event.key, level, player)
        if event.type == KEYDOWN and game_state == GAME_STATES['main']:
            game_state = handle_key(game_state, config, event.key, level, player)
    return game_state


def handle_key(game_state, config, event_key, level, player):
    dimensions = level.map.dimensions
    map_width, map_height = dimensions['width'], dimensions['height']
    tile_solids = level.map.tile_solids
    if event_key == K_UP and player.y > 0:
        tile_up_index = level.map.get_index(player.x, player.y - 1)
        if not tile_solids[tile_up_index]:
            player.y -= 1
    if event_key == K_DOWN and player.y < map_height - 1:
        tile_down_index = level.map.get_index(player.x, player.y + 1)
        if not tile_solids[tile_down_index]:
            player.y += 1
    if event_key == K_LEFT and player.x > 0:
        tile_left_index = level.map.get_index(player.x - 1, player.y)
        if not tile_solids[tile_left_index]:
            player.x -= 1
    if event_key == K_RIGHT and player.x < map_width - 1:
        tile_right_index = level.map.get_index(player.x + 1, player.y)
        if not tile_solids[tile_right_index]:
            player.x += 1
    return game_state


def handle_dialog(game_state, config, event_key, level, player):
    if event_key == K_RETURN or event_key == K_SPACE:
        game_state = GAME_STATES['main']
        config.questions.next()
    questions = config.questions
    if event_key == K_UP and questions.choice > 0:
        questions.choice -= 1
    if event_key == K_DOWN and questions.choice < questions.get_choices_length() - 1:
        questions.choice += 1
    return game_state
