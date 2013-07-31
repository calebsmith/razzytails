import os
 
import pygame

from yape.components import LoadableComponent
from json_janitor.schema import Schema
from json_janitor.defs import AnyInteger, AnyString


# Path directories
PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')


class Config(LoadableComponent):

    path = 'config'
    location = 'config.json'
    schema = Schema({
        u'start': AnyString,
        u'player_image': AnyString,
        u'splash_image': AnyString,
        u'endscreen_image': AnyString,
        u'score_font': [AnyString, AnyInteger],
        u'music': AnyString,
        u'popup_box': {
            u'x': AnyInteger,
            u'y': AnyInteger,
            u'char_width': AnyInteger,
            u'char_height': AnyInteger,
        },
        u'keypress_repeat': {
            u'delay': AnyInteger,
            u'interval': AnyInteger,
        },
        u'questions': AnyString,
        u'monster_delay': AnyInteger,
        u'joystick': {
            u'delay': AnyInteger,
            u'pressed': AnyInteger,
        }
    })

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

