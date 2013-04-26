import pygame


class Dispatch(object):
    """
    An event dispatcher that registers event listeners and dispatchs events to
    them based on the current game state.
    """

    listeners = {}

    class RequiresStateMachine(Exception):
        pass

    def __init__(self):
        self.game_state = None

    def register(self, state, listener, event_type=None):
        """
        Given a `state` name and a `listener` function, registers the listener
        for calling when the game is in that state.
        """
        existing = self.listeners.get(state, [])
        existing.append(listener)
        event_type = event_type or pygame.constants.KEYDOWN
        self.listeners[(state, event_type)] = existing

    def attach_state_machine(self, game_state):
        self.game_state = game_state

    def handle_events(self, config, level, player):
        if not self.game_state:
            raise self.RequiresStateMachine(
                'Dispatcher has no state machine attached'
            )
        for event in pygame.event.get():
            self.dispatch(event, self.game_state, config, level, player)

    def dispatch(self, event, *args, **kwargs):
        if not self.game_state:
            raise self.RequiresStateMachine(
                'Dispatcher has no state machine attached'
            )
        state = self.game_state.state
        listeners = self.listeners.get((state, event.type), [])
        for listener in listeners:
            listener(event, *args, **kwargs)

dispatcher = Dispatch()


def register_listener(states, event_type=None):

    def decorator(f):

        if not getattr(f, 'registered', False):
            for state in states:
                dispatcher.register(state, f, event_type)
            f.registered = True

        def _(*args, **kwargs):
            f(*args, **kwargs)
        return _
    return decorator
