#!/usr/bin/env python

from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT
from utils import get_map_index


def handle_key(event_key, level, player):
    dimensions = level.map.dimensions
    map_width, map_height = dimensions['width'], dimensions['height']
    tile_solids = level.map.tile_solids
    if event_key == K_UP and player.y > 0:
        tile_up_index = get_map_index(map_width, player.x, player.y - 1)
        if not tile_solids[tile_up_index]:
            player.y -= 1
    if event_key == K_DOWN and player.y < map_height - 1:
        tile_down_index = get_map_index(map_width, player.x, player.y + 1)
        if not tile_solids[tile_down_index]:
            player.y += 1
    if event_key == K_LEFT and player.x > 0:
        tile_left_index = get_map_index(map_width, player.x - 1, player.y)
        if not tile_solids[tile_left_index]:
            player.x -= 1
    if event_key == K_RIGHT and player.x < map_width - 1:
        tile_right_index = get_map_index(map_width, player.x + 1, player.y)
        if not tile_solids[tile_right_index]:
            player.x += 1
