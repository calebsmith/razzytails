#!/usr/bin/env python
from loaders import initialize, load_level
from logic import logic
from graphics import render
from assets import Player
from const import ASSETS_DIR


def main():
    # Initialize display screen and load assets
    game_state, dispatcher, manager, screen, config = initialize(ASSETS_DIR)
    player = Player()
    level = load_level(manager, config, player)
    # Run game loop
    game_loop(game_state, dispatcher, screen, config, level, player)


def game_loop(game_state, dispatcher, screen, config, level, player):
    while not game_state.is_state('exit'):
        dispatcher.handle_events(game_state, config, level, player)
        logic(game_state, config, level, player)
        render(game_state, screen, config, level, player)

if __name__ == "__main__":
    main()

