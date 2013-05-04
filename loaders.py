#!usr/bin/env python
import pygame

from game_assets import Config, Level, Screen, Player
from game_state import game_state
from listeners import dispatcher


def initialize():
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a 5-item tuple in the form of:
        (game_state, dispatcher, screen, config, player)
    """
    # Initialize pygame and pygame mixer
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.joystick.Joystick(0).init()
    except:
        pass
    # Load configuration file for various settings
    config = Config()
    # by default the key repeat is disabled, call set_repeat() to enable it
    delay = config.keypress_repeat['delay']
    interval = config.keypress_repeat['interval']
    pygame.key.set_repeat(delay, interval)
    # Create a screen to get a display context
    screen = Screen(config.screen)
    screen.set_background('white')
    # Load the image, font, and sound assets of the config file
    config.load_assets()
    # Create the player
    player = Player()
    # Play background music if possible
    if config.music:
        try:
            pygame.mixer.music.load(config.music)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    dispatcher.attach_state_machine(game_state)
    return game_state, dispatcher, screen, config, player


def load_level(screen, config, player):
    """
    Load the level from the config. Set the player's start location
    according to the level's map.
    """
    level = Level(config)
    # Place player at the start location
    player.x = level.map.player_start['x']
    player.y = level.map.player_start['y']
    screen.attach_level(level)
    return level
