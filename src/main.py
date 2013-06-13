#!/usr/bin/env python

from yape.initialize import initialize

from state import game_state
from listeners import dispatcher
from config import ASSETS_DIR, Config
from assets import Player, Level, Questions
from logic import logic
from graphics import render


def main():
    # Initialize display screen and load assets
    game_data = initialize(game_state, dispatcher, Config, ASSETS_DIR)
    # Load the player, questions, and level before the game begins
    player = Player(game_data.manager)
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

