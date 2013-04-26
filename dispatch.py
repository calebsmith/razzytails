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

    def register(self, state, listener):
        """
        Given a `state` name and a `listener` function, registers the listener
        for calling when the game is in that state.
        """
        existing = self.listeners.get(state, [])
        existing.append(listener)
        self.listeners[state] = existing

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
        for listener in self.listeners[state]:
            listener(event, *args, **kwargs)

dispatcher = Dispatch()


def register_listener(states):

    def decorator(f):

        if not getattr(f, 'registered', False):
            for state in states:
                dispatcher.register(state, f)
            f.registered = True

        def _(*args, **kwargs):
            f(*args, **kwargs)
        return _
    return decorator
