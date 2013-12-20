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
