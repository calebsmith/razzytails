#!/usr/bin/env python
from loaders import initialize, load_level
from logic import logic
from graphics import render
from assets import Player


def main():
    # Initialize display screen and load assets
    game_state, dispatcher, screen, config = initialize()
    player = Player()
    level = load_level(screen, config, player)
    # Run game loop
    game_loop(game_state, dispatcher, screen, config, level, player)


def game_loop(game_state, dispatcher, screen, config, level, player):
    while not game_state.is_state('exit'):
        dispatcher.handle_events(config, level, player)
        logic(game_state, config, level, player)
        render(game_state, screen, config, level, player)

if __name__ == "__main__":
    main()
