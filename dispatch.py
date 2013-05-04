import pygame
from fsm import RequiresStateMachine


class Dispatch(object):
    """
    An event dispatcher that registers event listeners and dispatchs events to
    them based on the current game state.
    """

    listeners = {}
    state_machine = None

    def register(self, state, listener, event_type=None):
        """
        Given a `state` name and a `listener` function, registers the listener
        for calling when the game is in that state.
        """
        event_type = event_type or pygame.constants.KEYDOWN
        existing = self.listeners.get((state, event_type), [])
        existing.append(listener)
        self.listeners[(state, event_type)] = existing

    def attach_state_machine(self, state_machine):
        self.state_machine = state_machine

    def handle_events(self, *args, **kwargs):
        if not self.state_machine:
            raise RequiresStateMachine(
                'Dispatcher has no state machine attached'
            )
        for event in pygame.event.get():
            self.dispatch(event, *args, **kwargs)

    def dispatch(self, event, *args, **kwargs):
        if not self.state_machine:
            raise RequiresStateMachine(
                'Dispatcher has no state machine attached'
            )
        state = self.state_machine.state
        for listener in self.listeners.get((state, event.type), []):
            listener(event, self.state_machine, *args, **kwargs)

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

            def _(*args, **kwargs):
                f(*args, **kwargs)
            return _
        return decorator

dispatcher = Dispatch()
