import os

import pygame

from yape.screen import Screen
from yape.manager import Manager

from assets import Level


def initialize(game_state, ConfigClass, dispatcher, assets_path):
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a 4-item tuple in the form of:
        (game_state, dispatcher, manager, screen, config)
    """
    # Initialize pygame and pygame mixer
    pygame.init()
    pygame.mixer.init()
    # TODO: Joystick support is very experimental
    try:
        pygame.joystick.Joystick(0).init()
    except:
        pass
    manager = Manager(assets_path)
    # Create a screen to get a display context
    screen = Screen(manager)
    # Load configuration file for various settings
    config = ConfigClass(manager)
    return game_state, config, dispatcher, manager, screen


def load_level(manager, config, player):
    """
    Load the level from the config. Set the player's start location
    according to the level's map.
    """
    level = Level(manager, config)
    # Place player at the start location
    player.x = level.map.player_start['x']
    player.y = level.map.player_start['y']
    return level
