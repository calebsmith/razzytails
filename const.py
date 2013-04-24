import os

# Path directories
PROJECT_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')

CONFIG_DIR = ASSETS_DIR
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
MAPS_DIR = os.path.join(ASSETS_DIR, 'maps')


# FSM nodes
MAIN_STATE = 0
EXIT_STATE = 1
DIALOG_STATE = 2
GAME_STATES = {
    'main': MAIN_STATE,
    'exit': EXIT_STATE,
    'dialog': DIALOG_STATE,
}
