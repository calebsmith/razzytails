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


# FSM nodes and transitions
FSM_INITIAL = 'main'
FSM_TRANSITIONS = [
    {
        'name': 'answer',
        'source': 'dialog',
        'destination': 'main',
    },
    {
        'name': 'popup',
        'source': 'main',
        'destination': 'dialog'
    },
    {
        'name': 'exit',
        'source': 'main',
        'destination': 'exit'
    },
    {
        'name': 'exit',
        'source': 'dialog',
        'destination': 'exit'
    },
]
