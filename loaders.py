import pygame

from yape.screen import Screen
from assets import Config, Level
from state import game_state
from listeners import dispatcher
from const import CONFIG_DIR


def initialize():
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a 4-item tuple in the form of:
        (game_state, dispatcher, screen, config)
    """
    # Initialize pygame and pygame mixer
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.joystick.Joystick(0).init()
    except:
        pass
    # Create a screen to get a display context
    screen = Screen(path=CONFIG_DIR, location='screen.json')
    screen.set_background('white')
    # Load configuration file for various settings
    config = Config()
    delay = config.keypress_repeat['delay']
    interval = config.keypress_repeat['interval']
    pygame.key.set_repeat(delay, interval)
    # Play background music if possible
    if config.music:
        try:
            pygame.mixer.music.load(config.music)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    return game_state, dispatcher, screen, config


def load_level(screen, config, player):
    """
    Load the level from the config. Set the player's start location
    according to the level's map.
    """
    level = Level(config)
    # Place player at the start location
    player.x = level.map.player_start['x']
    player.y = level.map.player_start['y']
    return level
