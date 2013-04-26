#!/usr/bin/env python
import pygame

from loaders import initialize, load_level
from graphics import render


def main():
    # Initialize display screen and load assets
    game_state, dispatcher, screen, config, player = initialize()
    level = load_level(config, player)
    # Run game loop
    game_loop(game_state, dispatcher, screen, config, level, player)


def game_loop(game_state, dispatcher, screen, config, level, player):
    while game_state.state != 'exit':
        dispatcher.handle_events(config, level, player)
        if game_state.is_state('main'):
            player_coordinate = player.x, player.y
            for item in level.item_coordinates:
                if player_coordinate == item['coordinates']:
                    level.item_coordinates.remove(item)
                    item_obj = [x for x in level.items if x.id == item['id']][0]
                    game_state.popup_item(player, item_obj)

            ticks = pygame.time.get_ticks()
            for monster in level.monsters:
                if ticks > (monster.last_moved_at + config.monster_delay):
                    monster.last_moved_at = ticks
                    monster.move(level, player)

        render(game_state, screen, config, level, player)

if __name__ == "__main__":
    main()
