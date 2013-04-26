#!/usr/bin/env python
from loaders import initialize, load_level
from input_handlers import handle_events
from graphics import render


def main():
    # Initialize display screen and load assets
    game_state, screen, config, player = initialize()
    level = load_level(config.start, player)
    # Run game loop
    game_loop(game_state, screen, config, level, player)


def game_loop(game_state, screen, config, level, player):
    while game_state.state != 'exit':
        handle_events(game_state, config, level, player)
        player_coordinate = player.x, player.y
        for index, item in enumerate(level.map.item_coordinates):
            if player_coordinate in item['coordinates']:
                level.map.item_coordinates.remove(index)
                # perform dialog for the item
                game_state.popup()
        render(game_state, screen, config, level, player)

if __name__ == "__main__":
    main()
