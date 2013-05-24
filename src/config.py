import os
 
import pygame

from yape.asset_loaders import LoadableAsset

# Path directories
PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')


class Config(LoadableAsset):

    path = 'config'
    location = 'config.json'
    schema = [
        'start',
        'player_image',
        'splash_image',
        'endscreen_image',
        'score_font',
        'music',
        {
            'popup_box': [
                'x', 'y', 'char_width', 'char_height'
            ]
        },
        {
            'keypress_repeat': [
                'delay',
                'interval'
            ]
        },
        'questions',
        'monster_delay',
        {
            'joystick': [
                'delay',
                'pressed'
            ]
        }
    ]

    image_fields = [
        'player_image',
        'splash_image',
        'endscreen_image',
    ]

    font_fields = [
        'score_font',
    ]

    def post_process(self):
        delay = self.keypress_repeat['delay']
        interval = self.keypress_repeat['interval']
        pygame.key.set_repeat(delay, interval)
        # Play background music if possible
        if self.music:
            try:
                filename = self.music
                music_path_filename = os.path.join(self.manager.path, 'music', filename)
                pygame.mixer.music.load(music_path_filename)
                pygame.mixer.music.play(-1)
            except pygame.error:
                pass

