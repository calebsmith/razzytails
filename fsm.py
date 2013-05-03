from functools import partial


class FSM(object):
    """
    A simple finite state machine that defines a set of states and the
    transitions between those states. The constructor takes the name of the
    initial state, a list of transitions, and a dictionary of callbacks.
    `transitions` is a list of dictionaries with 'source', 'destination', and
    'name' keys. Transitions of the same name may have the different sources or
    map to different destinations.

    Callbacks have keys that correspond to transition names and are prefixed
    with 'on_' or 'on_before_'. For example, a transition named 'enter'
    could have the callbacks 'on_enter' and 'on_before_enter'. The
    'on_before' callbacks return True if the transition should occur or False
    to short circuit the impending transition. Return values of the 'on'
    callbacks are passed to the caller of the transition (e.g. result in the
    expression `result = fms.enter()` would be set to the return of `on_enter`)

    Transitions may take any positional or keyword arguments. These are passed
    to the associated callback(s) for the transition. In the above example, a
    call to fms.enter(score=10), would pass the score=10 kwarg to the
    `on_enter` and `on_before_enter` for handling.
    """

    # Tracks the set of possible states or "nodes" that the machine may enter
    possible_states = set()
    # Maintains the mapping of a source/transition name pair to a destination
    transitions = {}
    # Maintains the mapping of each callback's name to the callback function
    callbacks = {}
    # Maintains the mapping of each source to the list of possible transitions
    _source_to_names = {}

    class IllegalNameException(Exception):
        pass

    class IllegalCallbackException(Exception):
        pass

    class IllegalTransitionException(Exception):
        pass

    def __init__(self, initial, transitions=None, callbacks=None):
        # Define the initial state and store the transitions and callbacks if
        # provided
        self.state = initial
        self.possible_states.add(initial)
        callbacks = callbacks or {}
        transitions = transitions or []
        map(self.add_transition, transitions)
        map(lambda k_v: self.add_callback(*k_v), callbacks.items())

    def add_transition(self, transition):
        """
        Given a transition dictionary that defines a `source`, `name`, and
        `destination`, add the transition function with the `name` that moves
        the state from the `source` to the `destination`.

        An IllegalNameException is thrown if the transition name would override
        another method.
        """
        source, name = transition['source'], transition['name']
        destination = transition['destination']
        # Assure transition names won't override existing methods
        transition_names = [
            t_name for t_source, t_name in self.transitions.keys()
        ]
        reserved_methods = set(dir(self)).difference(transition_names)
        if name in reserved_methods:
            err_msg = u'The transition name `{0}` shadows an existing method'
            raise self.IllegalNameException(
                err_msg.format(name)
            )
        # Update transitions, possible_states
        self.transitions.update({
            (source, name): destination
        })
        existing_names = self._source_to_names.get(source, [])
        existing_names.append(name)
        self._source_to_names[source] = existing_names
        self.possible_states.add(source)
        self.possible_states.add(destination)
        if not hasattr(self, name):
            # Create a function for the transition
            func = partial(self._transition_function_factory, source, name)
            setattr(self, name, func)

    def add_callback(self, name, func):
        """
        Given a `name` and `func`, registers the `func` as a callback for the
        transition associated with `name`.

        An IllegalCallbackException is thrown if the callback name does not
        correspond to an existing transition. This is meant to safeguard
        against registering callbacks with incorrect names, which will never be
        called.
        """
        # Determine the name of the associated transition
        transition_name = name[3:]
        if transition_name.startswith('before_'):
            transition_name = transition_name[7:]
        transition_names = [
            t_name for t_source, t_name in self.transitions.keys()
        ]
        if transition_name not in transition_names:
            err_msg = u'Callback {0} can not be registered because {1} is not a transition name'
            raise self.IllegalCallbackException(
                err_msg.format(name, transition_name)
            )
        self.callbacks.update({
            name: func
        })

    def _transition_function_factory(self, source, name, *args, **kwargs):
        """
        Given an existing transition's `source` and `name` create a method with
        that name, that moves the state from the source to the destination
        state. When called, validates that the current state is the source
        state, and calls any registered callbacks for the transition.
        """
        destination = self.transitions.get((source, name), None)
        if destination is not None:
            if self.callbacks:
                resume = self._call_callback(name, 'before', *args, **kwargs)
                if resume:
                    self.state = destination
                    return self._call_callback(name, '', *args, **kwargs)
            else:
                self.state = destination
        else:
            err_msg = '{0} called when current state was {1}'
            raise self.IllegalTransitionException(
                err_msg.format(name, self.state)
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

    def is_state(self, check_state):
        """Checks if the current state is `check_state`"""
        return self.state == check_state

    def can(self, name):
        """
        Checks if the given `name` is a possible transition from the current
        state
        """
        return name in self._source_to_names[self.state]

    def __repr__(self):
        return u'State machine: ({0}) '.format(self.state) + u' '.join([
            state
            for state in self.possible_states
            if state != self.state
        ])

    def callbacks_display(self):
        return self.callbacks.keys()

    def transitions_display(self):
        return sorted([
            '{0}: {1} -> {2}'.format(name, source, destination)
            for (source, name), destination in self.transitions.items()
        ])
