import pyglet

class Scene(object):
    def __init__(self):
        self.depth_groups = {}

    def get_depth_group(self, z):
        index = -int(10.0 * z)
        depth_group = self.depth_groups.get(index)
        if depth_group is None:
            depth_group = pyglet.graphics.OrderedGroup(index)
            self.depth_groups[index] = depth_group
        return depth_group
