#!/usr/bin/env python

from loaders import initialize, load_level
from input_handlers import handle_events
from graphics import render


def main():
    # Initialize display screen, load config and game assets
    game_state, screen, config, player = initialize()
    level = load_level(config.start, player)
    # Run game loop
    game_loop(game_state, screen, config, level, player)


def game_loop(game_state, screen, config, level, player):
    while game_state.state != 'exit':
        handle_events(game_state, config, level, player)
        # FIXME: Remove when raspberries are removed
        player_coordinate = player.x, player.y
        if player_coordinate in level.map.raspberry_coordinates:
            player.raspberries += 1
            level.map.raspberry_coordinates.remove(player_coordinate)
            game_state.popup()
        #
        render(game_state, screen, config, level, player)

if __name__ == "__main__":
    main()
