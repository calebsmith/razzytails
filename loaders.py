import os

import pygame

from yape.screen import Screen
from assets import Config, Level
from state import game_state
from listeners import dispatcher
from const import CONFIG_DIR, IMAGES_DIR, FONTS_DIR


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
    dispatcher.attach_state_machine(game_state)
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

# FIXME: These utility functions should be part of the yape engine. Leaving
# here for now since they are tied to IMAGES_DIR and FONTS_DIR


def load_image(filename):
    image_file = os.path.join(IMAGES_DIR, filename)
    try:
        image = pygame.image.load(image_file).convert_alpha()
    except (IOError, pygame.error):
        print 'Image file {0} not found'.format(image_file)
        image = None
    return (filename, image)


def load_font(filename, font_size=16):
    font_file = os.path.join(FONTS_DIR, filename)
    try:
        font = pygame.font.Font(font_file, font_size)
    except (IOError, pygame.error):
        print 'Font file {0} not found'.format(font_file)
        font = None
    return (filename, font)
