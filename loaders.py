#!usr/bin/env python
import pygame

from game_assets import Config, Level, Screen, Player
from game_state import game_state


def initialize():
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a 4-item tuple in the form of:
        (game_state, screen, config, player)
    """
    # Initialize pygame and pygame mixer
    pygame.init()
    pygame.mixer.init()
    config = Config()
    # by default the key repeat is disabled, call set_repeat() to enable it
    delay = config.keypress_repeat['delay']
    interval = config.keypress_repeat['interval']
    pygame.key.set_repeat(delay, interval)
    # Create a screen to get a display context
    screen = Screen(config.screen)
    screen.set_background('black')
    # Create the player
    player = Player()
    # Play background music if possible
    if config.music:
        try:
            pygame.mixer.music.load(config.music)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    return game_state, screen, config, player


def load_level(level_filename, player):
    """
    Load the level from the level_filename. Set the player's start location
    according to the level's map.
    """
    level = Level(level_filename)
    # Place player at the start location
    player.x = level.map.player_start['x']
    player.y = level.map.player_start['y']
    return level
