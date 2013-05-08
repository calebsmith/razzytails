from contextlib import contextmanager

import pygame
from pygame import Surface, display

from const import CONFIG_DIR
from asset_loaders import Asset, LoadableAsset


class Screen(LoadableAsset):
    path = CONFIG_DIR
    location = 'screen.json'
    schema = [
        'title',
        'width',
        'height',
        'tile_width',
        'tile_height',
        'map_display_width',
        'map_display_height',
    ]

    background = None

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self._create_context()

    def _create_context(self):
        display.set_caption(self.title)
        self.context = display.set_mode((self.width, self.height))

    def handle(self, data):
        super(Screen, self).handle(data)
        self.camera = Camera(data)

    def set_background(self, color='black'):
        background = Surface(self.context.get_size()).convert()
        background.fill(self.get_color(color))
        self.background = background

    def attach_level(self, level):
        self.camera.attach_level(level)

    @contextmanager
    def display_cycle(self):
        """
        A context manager that applies the background to the screen, calls the
        display functions within the block and then flips the display.
        """
        if self.background:
            self.context.blit(self.background, (0, 0))
        yield
        pygame.display.flip()

    def get_color(self, color):
        return pygame.color.THECOLORS.get(color, None) \
            or pygame.color.THECOLORS['black']

    def get_surface(self, width, height):
        return Surface((width, height))

    def draw_tile_relative(self, image, player, coordinates, surface=None):
        x, y = coordinates
        x_offset, y_offset = self.camera.get_tile_offset(player)
        rel_x, rel_y = x + x_offset, y + y_offset
        if (rel_x >= 0 and rel_x < self.map_display_width and
                rel_y >= 0 and rel_y < self.map_display_height):
            self.draw_tile(
                image, (x + x_offset, y + y_offset), surface=surface
            )

    def draw_tile(self, image, coordinates, surface=None):
        x, y = coordinates
        rel_x, rel_y = x * self.tile_width, y * self.tile_height
        self.draw(image, (rel_x, rel_y), surface=surface)

    def draw(self, image, coordinates, surface=None):
        surface = surface or self.context
        if image:
            surface.blit(image, coordinates)

    def draw_text(self, font, label, coordinates, color=None, surface=None):
        surface = surface or self.context
        if all((font, label)):
            text = font.render(label, True, self.get_color(color or 'white'))
            textpos = text.get_rect()
            textpos.move_ip(*coordinates)
            surface.blit(text, textpos)


class Camera(Asset):

    X = 'x'
    Y = 'y'

    def __init__(self, *args, **kwargs):
        super(Camera, self).__init__(*args, **kwargs)
        self.map_display_mid_x = self.map_display_width / 2
        self.map_display_mid_y = self.map_display_height / 2

    def attach_level(self, level):
        self.level = level

    def _get_offset_value(self, dimension, value, max_value):
        """
        Determine the display offset of the player or map tile based on the
        current level and player cooridnates
        """
        if dimension == 'x':
            med_display_mid = self.map_display_mid_x
            max_display_value = self.map_display_width
        else:
            med_display_mid = self.map_display_mid_y
            max_display_value = self.map_display_height
        if value < med_display_mid:
            return 0
        elif value < max_value - med_display_mid:
            return med_display_mid - value
        return max_display_value - max_value

    def _get_x_offset_value(self, value, max_value):
        return self._get_offset_value(self.X, value, max_value)

    def _get_y_offset_value(self, value, max_value):
        return self._get_offset_value(self.Y, value, max_value)

    def get_tile_offset(self, player):
        dimensions = self.level.map.dimensions
        return (
            self._get_x_offset_value(player.x, dimensions['width']),
            self._get_y_offset_value(player.y, dimensions['height'])
        )
