import pygame

from utils import get_color, get_image, get_font, get_display_coordinates, word_wrap


def draw_image(surface, obj, image_name, coordinates):
    image = get_image(obj, image_name)
    if image and surface:
        surface.blit(image, coordinates)


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
            display_x, display_y = get_display_coordinates(
                config, (player.x, player.y), (map_width, map_height)
            )
            current_index = level.map.get_index(
                map_x + (player.x - display_x), map_y + (player.y - display_y)
            )
            image_filename = tile_legend.get(unicode(tiles[current_index]), '')
            screen.context.blit(
                level.map.images[image_filename], (
                    map_x * config.screen['tile_width'],
                    map_y * config.screen['tile_height']
                )
            )


def display_player(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    display_x, display_y = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    draw_image(
        screen.context, config, config.player_image, (
            display_x * config.screen['tile_width'],
            display_y * config.screen['tile_height']
        )
    )


def display_monsters(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset, y_offset = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    for monster in level.monsters:
        display_x = monster.x - (player.x - x_offset)
        display_y = monster.y - (player.y - y_offset)
        if (display_x >= 0 and display_x < config.screen['map_display_width'] and
                display_y >= 0 and display_y < config.screen['map_display_height']):
            draw_image(
                screen.context, level, monster.image, (
                    display_x * config.screen['tile_width'],
                    display_y * config.screen['tile_height']
                )
            )


def display_items(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset, y_offset = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    for item_coords in level.item_coordinates:
        display_x = item_coords['coordinates'][0] - (player.x - x_offset)
        display_y = item_coords['coordinates'][1] - (player.y - y_offset)
        if (display_x >= 0 and display_x < config.screen['map_display_width'] and
                display_y >= 0 and display_y < config.screen['map_display_height']):
            item = next((x for x in level.items if x.id == item_coords['id']), None)
            draw_image(
                screen.context, level, item.image, (
                    display_x * config.screen['tile_width'],
                    display_y * config.screen['tile_height']
                )
            )


def display_player_items(game_state, screen, config, level, player):
    draw_text(
        screen.context, config, config.score_font, 'Inventory:', (0, 420),
        color=get_color('black')
    )
    for index, item in enumerate(player.items):
        draw_image(screen.context, level, item.image, (index * 32, 440))


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
        screen.context.blit(message_surface, (box_x, box_y))


def draw_splash(game_state, screen, config):
    width = config.screen['width']
    height = config.screen['height']
    message_surface = pygame.Surface((width, height))
    origin = (0, 0)
    draw_image(message_surface, config, config.splash_image, origin)
    screen.context.blit(message_surface, origin)


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
        draw_splash(game_state, screen, config)
    if game_state.is_state('item'):
        draw_popup(
            game_state, screen, config, level, player,
            player.current_item.message
        )
    pygame.display.flip()
