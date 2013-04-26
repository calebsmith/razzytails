import pygame

from utils import get_color, get_image, get_font, get_display_coordinates


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
        screen.context, config, 'razzy.png', (
            display_x * config.screen['tile_width'],
            display_y * config.screen['tile_height']
        )
    )


def display_monsters(game_state, screen, config, level, player):
    # don't let monsters move during dialog boxes
    if game_state.state != 'main':
        return
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset, y_offset = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    ticks = pygame.time.get_ticks()

    for monster in level.monsters:
        if ticks > (monster.last_moved_at + config.monster_delay):
            monster.last_moved_at = ticks
            monster.move(level, player)
        display_x = monster.x - (player.x - x_offset)
        display_y = monster.y - (player.y - y_offset)
        if (display_x >= 0 and display_x < config.screen['map_display_width'] and
                display_y >= 0 and display_y < config.screen['map_display_height']):
            draw_image(
                screen.context, config, monster.image[0], (
                    display_x * config.screen['tile_width'],
                    display_y * config.screen['tile_height']
                )
            )


def display_items(game_state, screen, config, level, player):
    map_width, map_height = level.map.dimensions['width'], level.map.dimensions['height']
    x_offset, y_offset = get_display_coordinates(
        config, (player.x, player.y), (map_width, map_height)
    )
    for item_coords in level.map.item_coordinates:
        display_x = item_coords['coordinates'][0] - (player.x - x_offset)
        display_y = item_coords['coordinates'][1] - (player.y - y_offset)
        if (display_x >= 0 and display_x < config.screen['map_display_width'] and
                display_y >= 0 and display_y < config.screen['map_display_height']):
            item = next((x for x in level.items if x.id == item_coords['id']), None)
            draw_image(
                screen.context, config, item.image[0], (
                    display_x * config.screen['tile_width'],
                    display_y * config.screen['tile_height']
                )
            )


def draw_dialog(game_state, screen, config, level, player, strings):
    # Create the black surface for the dialog area to go onto
    char_width = config.dialog_box['char_width']
    char_height = config.dialog_box['char_height']
    x_margin, y_margin = 10, 10
    message_surface = pygame.Surface(
        (10 * char_width + x_margin * 2, 25 * char_height + y_margin * 2)
    )
    box_x, box_y = config.dialog_box['x'], config.dialog_box['y']
    for index, string in enumerate(strings):
        draw_text(
            message_surface, config, config.score_font, string,
            (x_margin, y_margin + index * 20)
        )
        screen.context.blit(message_surface, (box_x, box_y))


def render(game_state, screen, config, level, player):
    screen.context.blit(screen.background, (0, 0))
    display_map(game_state, screen, config, level, player)
    display_items(game_state, screen, config, level, player)
    display_monsters(game_state, screen, config, level, player)
    display_player(game_state, screen, config, level, player)
    if game_state.is_state('dialog'):
        draw_dialog(
            game_state, screen, config, level, player,
            config.questions.get_question_display()
        )
    pygame.display.flip()
