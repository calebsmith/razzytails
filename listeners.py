from pygame.constants import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_SPACE,
    KEYDOWN, K_ESCAPE, QUIT)
from pygame import JOYAXISMOTION

from dispatch import dispatcher, register_listener
from movement import move_left, move_right, move_up, move_down


@register_listener(['splash'])
def splash_listener(event, game_state, *args, **kwargs):
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        game_state.start()


@register_listener(['main', 'question', 'item', 'splash'])
def quit_esc_listener(event, game_state, *args, **kwargs):
    if event.key == K_ESCAPE:
        game_state.exit()


@register_listener(['main', 'question', 'item'], QUIT)
def quit_x_listener(event, game_state, *args, **kwargs):
    game_state.exit()


@register_listener(['main'], KEYDOWN)
def move_player_listener(event, game_state, config, level, player):
    dimensions = level.map.dimensions
    map_width, map_height = dimensions['width'], dimensions['height']
    tile_solids = level.map.tile_solids

    event_key = event.key
    if event_key == K_UP and player.y > 0:
        move_up(level, player, tile_solids)
    if event_key == K_DOWN and player.y < map_height - 1:
        move_down(level, player, tile_solids)
    if event_key == K_LEFT and player.x > 0:
        move_left(level, player, tile_solids)
    if event_key == K_RIGHT and player.x < map_width - 1:
        move_right(level, player, tile_solids)


@register_listener(['main'], JOYAXISMOTION)
def move_player_joystick_listener(event, game_state, config, level, player):
    dimensions = level.map.dimensions
    map_width, map_height = dimensions['width'], dimensions['height']
    tile_solids = level.map.tile_solids

    value = event.value
    if event.axis == 0:
        if value > 0.75 and player.x < map_width - 1:
            move_right(level, player, tile_solids)
        elif value < -0.75 and player.x > 0:
            move_left(level, player, tile_solids)
    elif event.axis == 1:
        if value > 0 and player.y > 0:
            move_up(level, player, tile_solids)
        elif player.y < map_height - 1:
            move_down(level, player, tile_solids)


@register_listener(['question'])
def select_answer_listener(event, game_state, config, level, player):
    event_key = event.key
    questions = config.questions
    if event_key == K_RETURN or event_key == K_SPACE:
        game_state.answer(questions.is_correct(), level, player)
        questions.next()
    num_choices = questions.get_choices_length()
    if event_key == K_UP and questions.choice > 0:
        questions.choice -= 1
    if event_key == K_DOWN and questions.choice < num_choices - 1:
        questions.choice += 1


@register_listener(['item'])
def item_collected_listener(event, game_state, config, level, player):
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        game_state.item_collected()
