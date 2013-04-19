#!/usr/bin/env python

import sys
import time

import pygame
from pygame.constants import KEYUP, KEYDOWN, K_ESCAPE, QUIT

from loaders import initialize, load_map
from input_handlers import handle_key
from graphics import render


def main(*args):
    # Initialize display screen and load assets
    config, screen = initialize()
    level = load_map('map1.json')
    player = level.player_start
    player['raspberries'] = 0
    while True:
        # Exit on escape key or X
        for event in pygame.event.get():
            pressed_escape = event.type == KEYUP and event.key == K_ESCAPE
            if pressed_escape or event.type == QUIT:
                return
            if event.type == KEYDOWN:
                handle_key(event.key, level, player)
        time.sleep(0.05)
        player_coordinate = player['x'], player['y']
        if player_coordinate in level.map.raspberry_coordinates:
            player['raspberries'] += 1
            level.map.raspberry_coordinates.remove(player_coordinate)
        render(screen, config, level, player)


if __name__ == "__main__":
    main(sys.argv)
