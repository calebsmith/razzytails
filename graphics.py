import pygame

from utils import get_color, get_font


def draw_text(surface, obj, font_name, label, coordinates, color=None):
    font = get_font(obj, font_name)
    if all((surface, font, label)):
        text = font.render(label, True, color or get_color('white'))
        textpos = text.get_rect()
        textpos.move_ip(*coordinates)
        surface.blit(text, textpos)


def display_map(game_state, screen, config, level, player):
    tiles = level.map.tiles
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    tile_legend = level.map.legend
    for map_y in range(0, config.screen['map_display_height']):
        for map_x in range(0, config.screen['map_display_width']):
            x_offset, y_offset = screen.camera.get_tile_offset(player)
            current_index = level.map.get_index(
                map_x - x_offset, map_y - y_offset
            )
            image_filename = tile_legend.get(unicode(tiles[current_index]), '')
            image = level.map.images[image_filename]
            screen.draw_tile(image, (map_x, map_y))


def display_player(game_state, screen, config, level, player):
    image = config.images.get(config.player_image, None)
    screen.draw_tile_relative(image, player, (player.x, player.y))


def display_monsters(game_state, screen, config, level, player):
    for monster in level.monsters:
        image = level.images.get(monster.image)
        screen.draw_tile_relative(image, player, (monster.x, monster.y))


def display_items(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset, y_offset = screen.camera.get_tile_offset(player)
    for item_coords in level.item_coordinates:
        item = next((x for x in level.items if x.id == item_coords['id']), None)
        image = level.images.get(item.image)
        screen.draw_tile_relative(image, player, item_coords['coordinates'])


def display_player_items(game_state, screen, config, level, player):
    draw_text(
        screen.context, config, config.score_font, 'Inventory:', (0, 420),
        color=get_color('black')
    )
    for index, item in enumerate(player.items):
        image = level.images.get(item.image, None)
        # Position each item from left to right with respect to ordering and
        # on the bottom tile, adjusted by 8 for some padding
        x = index * screen.tile_width
        y = screen.height - screen.tile_height - 8
        screen.draw(image, (x, y))


def draw_popup(game_state, screen, config, level, player, strings):
    # Create the black surface for the popup area to go onto
    char_width = config.popup_box['char_width']
    char_height = config.popup_box['char_height']
    x_margin, y_margin = 10, 10
    message_surface = pygame.Surface(
        (10 * char_width + x_margin * 2, 25 * char_height + y_margin * 2)
    )
    box_x, box_y = config.popup_box['x'], config.popup_box['y']
    for index, string in enumerate(strings):
        draw_text(
            message_surface, config, config.score_font, string,
            (x_margin, y_margin + index * 20)
        )
        screen.draw(message_surface, (box_x, box_y))


def draw_splash(game_state, screen, config, image):
    width = config.screen['width']
    height = config.screen['height']
    message_surface = pygame.Surface((width, height))
    origin = (0, 0)
    if image:
        message_surface.blit(image, origin)
    screen.draw(message_surface, origin)


def render(game_state, screen, config, level, player):
    screen.context.blit(screen.background, (0, 0))
    display_map(game_state, screen, config, level, player)
    display_items(game_state, screen, config, level, player)
    display_monsters(game_state, screen, config, level, player)
    display_player(game_state, screen, config, level, player)
    display_player_items(game_state, screen, config, level, player)
    if game_state.is_state('question'):
        draw_popup(
            game_state, screen, config, level, player,
            config.questions.get_question_display()
        )
    if game_state.is_state('splash'):
        image = config.images.get(config.splash_image, None)
        draw_splash(game_state, screen, config, image)
    if game_state.is_state('endscreen'):
        image = config.images.get(config.endscreen_image, None)
        draw_splash(game_state, screen, config, image)
    if game_state.is_state('item'):
        draw_popup(
            game_state, screen, config, level, player,
            player.current_item.message
        )
    if game_state.is_state('info'):
        draw_popup(game_state, screen, config, level, player, [
            'Honey Badger got you! You lost all of your items', '',
            'Press <Enter> to return'
        ])
    pygame.display.flip()
