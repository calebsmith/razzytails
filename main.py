#!/usr/bin/env python
from loaders import initialize, load_map
from input_handlers import handle_events
from graphics import render


def main():
    # Initialize display screen and load assets
    screen, config, player = initialize()
    level = load_map(config.start, player)
    # Run game loop
    game_loop(screen, config, level, player)


def game_loop(screen, config, level, player):
    exit = False
    while not exit:
        exit = handle_events(config, level, player)
        player_coordinate = player.x, player.y
        if player_coordinate in level.map.raspberry_coordinates:
            player.raspberries += 1
            level.map.raspberry_coordinates.remove(player_coordinate)
        render(screen, config, level, player)


if __name__ == "__main__":
    main()
