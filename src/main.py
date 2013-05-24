#!/usr/bin/env python
import os

from yape.initialize import initialize
from logic import logic
from graphics import render
from assets import Config, Player, Level, Questions
from state import game_state
from listeners import dispatcher

# Path directories
PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')


def main():
    # Initialize display screen and load assets
    game_data = initialize(game_state, dispatcher, Config, ASSETS_DIR)
    player = Player(game_data.manager)
    # TODO: Joystick support is very experimental
    try:
        pygame.joystick.Joystick(0).init()
    except:
        pass
    questions = Questions(game_data.manager, game_data.config)
    level = Level(game_data.manager, game_data.config)
    # Place player at the start location
    player.x = level.map.player_start['x']
    player.y = level.map.player_start['y']
    # Run game loop
    game_loop('exit', game_data, questions, level, player)


def game_loop(exit_state, game_data, questions, level, player):
    while not game_data.state.is_state(exit_state):
        game_data.dispatcher.handle_events(game_data, questions, level, player)
        logic(game_data, questions, level, player)
        render(game_data, questions, level, player)

if __name__ == "__main__":
    main()

