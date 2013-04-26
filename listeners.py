from pygame.constants import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_SPACE,
    KEYDOWN, K_ESCAPE, QUIT)

from dispatch import dispatcher, register_listener


@register_listener(['main', 'dialog'])
def quit_listener(event, game_state, *args, **kwargs):
    pressed_escape = event.type == KEYDOWN and event.key == K_ESCAPE
    if pressed_escape or event.type == QUIT:
        game_state.exit()


@register_listener(['main'])
def move_player_listener(event, game_state, config, level, player):
    if event.type != KEYDOWN:
        return
    event_key = event.key
    dimensions = level.map.dimensions
    map_width, map_height = dimensions['width'], dimensions['height']
    tile_solids = level.map.tile_solids
    if event_key == K_UP and player.y > 0:
        tile_up_index = level.map.get_index(player.x, player.y - 1)
        if not tile_solids[tile_up_index]:
            player.y -= 1
    if event_key == K_DOWN and player.y < map_height - 1:
        tile_down_index = level.map.get_index(player.x, player.y + 1)
        if not tile_solids[tile_down_index]:
            player.y += 1
    if event_key == K_LEFT and player.x > 0:
        tile_left_index = level.map.get_index(player.x - 1, player.y)
        if not tile_solids[tile_left_index]:
            player.x -= 1
    if event_key == K_RIGHT and player.x < map_width - 1:
        tile_right_index = level.map.get_index(player.x + 1, player.y)
        if not tile_solids[tile_right_index]:
            player.x += 1


@register_listener(['dialog'])
def select_answer_listener(event, game_state, config, level, player):
    if event.type != KEYDOWN:
        return
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        game_state.answer()
        config.questions.next()
    questions = config.questions
    num_choices = questions.get_choices_length()
    if event_key == K_UP and questions.choice > 0:
        questions.choice -= 1
    if event_key == K_DOWN and questions.choice < num_choices - 1:
        questions.choice += 1
