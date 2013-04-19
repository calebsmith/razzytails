#!/usr/bin/env python

from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT
from utils import get_map_index


def handle_key(event_key, level, player):
    current_x = player['x']
    current_y = player['y']
    dimensions = level.map.dimensions
    map_width = dimensions['width']
    map_height = dimensions['height']
    tile_solids = level.map.tile_solids
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
