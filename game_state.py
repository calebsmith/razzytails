"""Defines transitions and callbacks for the game's fsm"""

from fsm import FSM


# FSM transitions and callbacks
transitions = [
    {
        'name': 'answer',
        'source': 'question',
        'destination': 'main',
    },
    {
        'name': 'item_collected',
        'source': 'item',
        'destination': 'main',
    },
    {
        'name': 'popup_question',
        'source': 'main',
        'destination': 'question'
    },
    {
        'name': 'popup_item',
        'source': 'main',
        'destination': 'item'
    },
    {
        'name': 'exit',
        'source': 'main',
        'destination': 'exit'
    },
    {
        'name': 'exit',
        'source': 'question',
        'destination': 'exit'
    },
    {
        'name': 'exit',
        'source': 'item',
        'destination': 'exit'
    },
]


def add_item_to_inventory(player, item):
    player.items.append(item)
    player.current_item = item
    return True


# No callbacks for now. Refer to fsm.py when implementating
callbacks = {'on_before_popup_item': add_item_to_inventory}

game_state = FSM('main', transitions, callbacks)
