import os

import pygame

from yape.screen import Screen
from assets import Config, Level
from state import game_state
from listeners import dispatcher
from yape.manager import Manager


def initialize(assets_path):
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a 4-item tuple in the form of:
        (game_state, dispatcher, manager, screen, config)
    """
    # Initialize pygame and pygame mixer
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.joystick.Joystick(0).init()
    except:
        pass
    manager = Manager(assets_path)
    # Create a screen to get a display context
    screen = Screen(manager)
    screen.set_background('white')
    # Load configuration file for various settings
    config = Config(manager)
    delay = config.keypress_repeat['delay']
    interval = config.keypress_repeat['interval']
    pygame.key.set_repeat(delay, interval)
    # Play background music if possible
    if config.music:
        try:
            filename = config.music
            music_path_filename = os.path.join(assets_path, 'music', filename)
            pygame.mixer.music.load(music_path_filename)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    return game_state, dispatcher, manager, screen, config


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
