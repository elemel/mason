class BlockGrid(object):
    def __init__(self):
        self._cells = {}

    def __getitem__(self, grid_position):
        return self._cells.get(grid_position)

    def __setitem__(self, grid_position, block_entity):
        if block_entity is None:
            self._cells.pop(grid_position, None)
        else:
            self._cells[grid_position] = block_entity

    def get_grid_position(self, world_position):
        world_x, world_y = world_position
        return int(round(world_x)), int(round(world_y))

    def get_world_position(self, grid_position):
        grid_x, grid_y = grid_position
        return float(grid_x), float(grid_y)
