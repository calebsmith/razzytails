def move_left(level, player, tile_solids):
    tile_left_index = level.map.get_index(player.x - 1, player.y)
    if not tile_solids[tile_left_index]:
        player.x -= 1


def move_right(level, player, tile_solids):
    tile_right_index = level.map.get_index(player.x + 1, player.y)
    if not tile_solids[tile_right_index]:
        player.x += 1


def move_up(level, player, tile_solids):
    tile_up_index = level.map.get_index(player.x, player.y - 1)
    if not tile_solids[tile_up_index]:
        player.y -= 1


def move_down(level, player, tile_solids):
    tile_down_index = level.map.get_index(player.x, player.y + 1)
    if not tile_solids[tile_down_index]:
        player.y += 1
