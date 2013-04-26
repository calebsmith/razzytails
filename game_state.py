"""Defines transitions and callbacks for the game's fsm"""

from fsm import FSM
from game_assets import Level

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
    {
        'name': 'start',
        'source': 'splash',
        'destination': 'main'
    }
]


def add_item_to_inventory(player, item):
    player.items.append(item)
    player.current_item = item
    return True


def handle_answer(is_correct, level, player):
    if is_correct:
        # Remove all monsters on the player's current location
        for monster in level.monsters:
            if (monster.x, monster.y) == (player.x, player.y):
                level.monsters.remove(monster)
    else:
        level.reset_items(player)
        level.reset_monsters()


# No callbacks for now. Refer to fsm.py when implementating
callbacks = {
    'on_before_popup_item': add_item_to_inventory,
    'on_answer': handle_answer,
}

game_state = FSM('splash', transitions, callbacks)
