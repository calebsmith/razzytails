#!/usr/bin/env python
from loaders import initialize, load_level
from input_handlers import handle_events
from graphics import render


def main():
    # Initialize display screen and load assets
    game_state, dispatcher, screen, config, player = initialize()
    level = load_level(config.start, player)
    # Run game loop
    game_loop(game_state, dispatcher, screen, config, level, player)


def game_loop(game_state, dispatcher, screen, config, level, player):
    while game_state.state != 'exit':
        dispatcher.handle_events(config, level, player)
        player_coordinate = player.x, player.y
        for item in level.map.item_coordinates:
            if player_coordinate == item['coordinates']:
                level.map.item_coordinates.remove(item)
                # perform dialog for the item
                game_state.popup()
        render(game_state, screen, config, level, player)

if __name__ == "__main__":
    main()
