import pygame
from fsm import RequiresStateMachine


class Dispatch(object):
    """
    An event dispatcher that registers event listeners and dispatchs events to
    them based on the current game state.
    """

    listeners = {}

    def register(self, state, listener, event_type=None):
        """
        Given a `state` name, a `listener` function, and an `event_type`,
        registers the listener for calling when the game is in the given state
        and the event type occurs.
        """
        event_type = event_type or pygame.constants.KEYDOWN
        existing = self.listeners.get((state, event_type), [])
        existing.append(listener)
        self.listeners[(state, event_type)] = existing

    def handle_events(self, game_data, *args, **kwargs):
        """
        Given the `game_data` and any args/kwargs, dispatch pygame events to
        the registered listeners for the current state based on the event_type
        """
        for event in pygame.event.get():
            self.dispatch(event, game_data, *args, **kwargs)

    def dispatch(self, event, game_data, *args, **kwargs):
        """
        Given the global state_machine, a pygame event, and any args/kwargs,
        call any registers that are registered for the state_machine's current
        state paired with the event type. Any args/kwargs are passed to the
        listeners
        """
        listeners = self.listeners.get((game_data.state.state, event.type), [])
        for listener in listeners:
            listener(event, game_data, *args, **kwargs)

    def register_listener(self, states, event_type=None):
        """
        Decorator that registers a listener. Takes a list of state strings to
        register the listener for. Optionally takes an event_type, which is the
        pygame event type that the listener should be called for. The default
        event type for the listener is KEYDOWN
        """

        def decorator(f):
            if not getattr(f, 'registered', False):
                for state in states:
                    self.register(state, f, event_type)
                f.registered = True
            return f
        return decorator

dispatcher = Dispatch()

