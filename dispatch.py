class Dispatch(object):
    """
    An event dispatcher that registers event listeners and dispatchs events to
    them based on the current game state.
    """

    listeners = {}

    def __init__(self, game_state):
        self.game_state = game_state

    def register(self, state, listener):
        """
        Given a `state` name and a `listener` function, registers the listener
        for calling when the game is in that state.
        """
        existing = self.listeners.get(state, [])
        existing.append(listener)
        self.listeners[state] = existing

    def dispatch(self, event, *args, **kwargs):
        state = self.game_state.state
        for listener in self.listeners[state]:
            listener(event, *args, **kwargs)
