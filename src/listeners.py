from pygame.constants import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_SPACE,
    KEYDOWN, K_ESCAPE, QUIT)
from pygame import time, JOYAXISMOTION

from yape.dispatch import dispatcher


@dispatcher.register_listener(['splash'])
def splash_listener(event, game_data, *args, **kwargs):
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        game_data.state.start()


@dispatcher.register_listener(['endscreen'])
def endscreen_listener(event, game_data, *args, **kwargs):
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        game_data.state.exit()


@dispatcher.register_listener(['main', 'question', 'item', 'splash'])
def quit_esc_listener(event, game_data, *args, **kwargs):
    if event.key == K_ESCAPE:
        game_data.state.exit()


@dispatcher.register_listener(['main', 'question', 'item'], QUIT)
def quit_x_listener(event, game_data, *args, **kwargs):
    game_data.state.exit()


@dispatcher.register_listener(['main'], KEYDOWN)
def move_player_listener(event, game_data, questions, level, player):
    event_key = event.key
    if event_key == K_UP:
        player.move_up(level)
    if event_key == K_DOWN:
        player.move_down(level)
    if event_key == K_LEFT:
        player.move_left(level)
    if event_key == K_RIGHT:
        player.move_right(level)


@dispatcher.register_listener(['main'], JOYAXISMOTION)
def move_player_joystick_listener(event, game_data, questions, level, player):
    config = game_data.config
    delay = config.joystick['delay']
    last_updated = player.last_updated
    value = event.value
    move = False

    if event.value == 0:
        player.neutral = True
        config.joystick['pressed'] = 0
        return
    if player.neutral:
        move = True
        player.neutral = False
    else:
        config.joystick['pressed'] += time.get_ticks()
        if last_updated:
            config.joystick['pressed'] -= last_updated

    if config.joystick['pressed'] > delay:
        move = True
        config.joystick['pressed'] -= delay

    if move:
        if event.axis == 0:
            if value > 0:
                player.move_right(level)
            else:
                player.move_left(level)
        elif event.axis == 1:
            if value > 0:
                player.move_up(level)
            else:
                player.move_down(level)


@dispatcher.register_listener(['question'])
def select_answer_listener(event, game_data, questions, level, player):
    config = game_data.config
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        game_data.state.answer(questions.is_correct(), level, player)
        questions.next()
    num_choices = questions.get_choices_length()
    if event_key == K_UP and questions.choice > 0:
        questions.choice -= 1
    if event_key == K_DOWN and questions.choice < num_choices - 1:
        questions.choice += 1


@dispatcher.register_listener(['item', 'info'])
def item_collected_listener(event, game_data, questions, level, player):
    event_key = event.key
    if event_key == K_RETURN or event_key == K_SPACE:
        if game_data.state.can('item_collected'):
            game_data.state.item_collected(level, player)
        else:
            game_data.state.info_closed()

