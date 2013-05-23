import pygame


def logic(game_data, level, player):
    if game_data.state.is_state('main'):
        player_on_item(game_data, level, player)
        player_on_monster(game_data, level, player)


def player_on_item(game_data, level, player):
    player_coordinate = player.x, player.y
    for item in level.item_coordinates:
        if player_coordinate == item['coordinates']:
            level.item_coordinates.remove(item)
            item_obj = [x for x in level.items if x.id == item['id']][0]
            game_data.state.popup_item(player, item_obj)


def player_on_monster(game_data, level, player):
    config = game_data.config
    ticks = pygame.time.get_ticks()
    for monster in level.monsters:
        if ticks > (monster.last_moved_at + config.monster_delay):
            monster.last_moved_at = ticks
            monster.move(level, player)
            if (monster.x, monster.y) == (player.x, player.y):
                game_data.state.popup_question()

