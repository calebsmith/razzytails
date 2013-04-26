from functools import partial


class FSM(object):
    """
    A simple finite state machine that defines a set of states and the
    transitions between those states. Constructor takes the name of the initial
    state, a list of transitions, and a dictionary of callbacks. transitions
    is a list of dictionaries with 'source', 'destination', and 'name' keys.
    Transitions of the same name may have the same source.

    Callbacks have keys that correspond to transition names and are prefixed
    with 'on_' or 'on_before_'. For example, a transition named 'enter'
    could have the callbacks 'on_enter' and 'on_before_enter'. The
    'on_before' callbacks return True if the transition should occur or False
    to short circuit the impending transition. Return values of the 'on'
    callbacks are passed to the caller of the transition (e.g. result in the
    expression `result = fms.enter()` would be set to the return of `on_enter`)
    """

    class IllegalNameException(Exception):
        pass

    class IllegalTransitionException(Exception):
        pass

    def is_state(self, check_state):
        """Checks if the current state is `check_state`"""
        return self.state == check_state

    def can(self, name):
        """
        Checks if the given `name` is a possible transition from the current
        state
        """
        if name not in self.transition_names:
            return False
        for transition in self.transitions:
            if name == transition['name']:
                break
        return self.state == transition['source']

    def __init__(self, initial, transitions, callbacks=None):
        # Define the initial state and store the transitions, callbacks,
        # possible states and the names of the transitions
        self.state = initial
        self.callbacks = callbacks or {}
        self.possible_states = set([
            transition['source'] for transition in transitions
        ] + [self.state])
        self.transitions = transitions
        self.transition_names = [
            transition['name'] for transition in transitions
        ]
        self._build_transitions()

    def _build_transitions(self):
        """Creates the transition functions of the FSM"""
        for transition in self.transitions:
            # Assure transition names won't override existing methods
            transition_name = transition['name']
            if transition_name in ('can', 'is_state'):
                err_msg = 'The transition name `{0}` shadows a built-in method'
                raise self.IllegalNameException(
                    err_msg.format(transition_name)
                )
            if not hasattr(self, transition_name):
                # Create a function for the transition
                func = partial(self._transition_function_factory, transition)
                setattr(self, transition_name, func)

    def _transition_function_factory(self, transition, *args, **kwargs):
        """
        Given a `transition` that defines a name, source and destination,
        create a method with that name, that moves the state from the source to
        the destination state. When called, validates that the current state
        is the source state, and calls any registered callbacks for the
        transition.
        """
        name, source = transition['name'], transition['source']
        destination = transition['destination']
        possible_sources = [
            trans['source']
            for trans in self.transitions
            if trans['name'] == name
        ]
        if self.state in possible_sources:
            if self.callbacks:
                resume = self._call_callback(name, 'before', *args, **kwargs)
                if resume:
                    self.state = destination
                    return self._call_callback(name, '', *args, **kwargs)
            else:
                self.state = destination
        else:
            err_msg = '{0} called when current state was not {1}'
            raise self.IllegalTransitionException(
                err_msg.format(name, transition['source'])
            )

    def _call_callback(self, transition_name, prefix, *args, **kwargs):
        """Calls the callback on behalf of the transition function"""
        if prefix:
            name_parts = ('on', prefix, transition_name)
        else:
            name_parts = ('on', transition_name)
        callback_name = '_'.join(name_parts)
        callback = self.callbacks.get(callback_name, None)
        if callback:
            return callback(*args, **kwargs)
        return True
