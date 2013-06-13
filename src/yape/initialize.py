from collections import namedtuple

import pygame

from yape.screen import Screen
from yape.manager import Manager


GameData = namedtuple('GameData',
    ['state', 'dispatcher', 'screen', 'config', 'manager']
)


def initialize(game_state, dispatcher, ConfigClass, assets_path):
    """
    Initializes pygame, loads the configuration files and creates a display
    context. Returns a GameData namedtuple with the following members:
        (game_state, dispatcher, screen, config, manager)
    """
    # Initialize pygame and pygame mixer
    pygame.init()
    pygame.mixer.init()
    manager = Manager(assets_path)
    # Create a screen to get a display context
    screen = Screen(manager)
    # Load configuration file for various settings
    config = ConfigClass(manager)
    return GameData(game_state, dispatcher, screen, config, manager)

