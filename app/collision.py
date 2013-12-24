from collections import defaultdict
from math import floor

def get_grid_box(box, cell_size=1.0):
    (x1, y1), (x2, y2) = box
    grid_x1 = int(floor(x1 / cell_size))
    grid_y1 = int(floor(y1 / cell_size))
    grid_x2 = int(floor(x2 / cell_size)) + 1
    grid_y2 = int(floor(y2 / cell_size)) + 1
    return (grid_x1, grid_y1), (grid_x2, grid_y2)

def generate_grid_positions(grid_box):
    (grid_x1, grid_y1), (grid_x2, grid_y2) = grid_box
    for grid_x in xrange(grid_x1, grid_x2):
        for grid_y in xrange(grid_y1, grid_y2):
            yield grid_x, grid_y

def intersects_box_box(box_a, box_b):
    (x1, y1), (x2, y2) = box_a
    (x3, y3), (x4, y4) = box_b
    return x1 < x4 and x3 < x2 and y1 < y4 and y3 < y2

def intersects_box_point(box, point):
    (x1, y1), (x2, y2) = box
    x, y = point
    return x1 < x < x2 and y1 < y < y2

class CollisionShape(object):
    def intersects(self, other):
        pass

    def get_bounding_box(self):
        pass

class CollisionPoint(CollisionShape):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def intersects(self, shape):
        return shape.intersects_point(self)

    def intersects_point(self, point):
        return False

    def intersects_box(self, box):
        return intersects_box_point(box, self)

    def get_bounding_box(self):
        return (self.x, self.y), (self.x, self.y)

class CollisionBox(CollisionShape):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __iter__(self):
        yield self.p1
        yield self.p2

    def intersects(self, shape):
        return shape.intersects_box(self)

    def intersects_box(self, box):
        return intersects_box_box(self, box)

    def intersects_point(self, point):
        return intersects_box_point(self, point)

    def get_bounding_box(self):
        return self.p1, self.p2

class CollisionBody(object):
    def __init__(self, shape, world=None, user_data=None):
        self._shape = shape
        self._bounding_box = shape.get_bounding_box()
        self._grid_box = (0, 0), (0, 0)
        self._world = None
        self._collisions = {}
        self.user_data = user_data
        self.world = world

    def delete(self):
        self.world = None

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def collisions(self):
        return self._collisions.itervalues()

    @property
    def collision_bodies(self):
        return self._collisions.iterkeys()

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, world):
        if world is not self._world:
            if self._world is not None:
                self._world._remove_body(self)
            self._world = world
            if self._world is not None:
                self._world._add_body(self)

    @property
    def dirty(self):
        return (self._world is not None and
                self in self._world._dirty_bodies)

    def intersects(self, other):
        (x1, y1), (x2, y2) = self._bounding_box
        (x3, y3), (x4, y4) = other._bounding_box
        return (intersects_box_box(self._bounding_box, other._bounding_box) and
                self._shape.intersects(other._shape))

    def touch(self):
        if self._world is not None:
            self._world._dirty_bodies.add(self)

    def _update_bounding_box(self):
        self._bounding_box = self._shape.get_bounding_box()

class Collision(object):
    def __init__(self, body_a, body_b):
        self._body_a = body_a
        self._body_b = body_b
        self.user_data = None

    @property
    def body_a(self):
        return self._body_a

    @property
    def body_b(self):
        return self._body_b

    @property
    def bodies(self):
        return self._body_a, self.body_b

    @property
    def dirty(self):
        return self._body_a.dirty or self._body_b.dirty

class CollisionListener(object):
    def on_collision_add(self, collision):
        pass

    def on_collision_update(self, collision):
        pass

    def on_collision_remove(self, collision):
        pass

class CollisionWorld(object):
    def __init__(self, cell_size=1.0, listener=None):
        self._cell_size = cell_size
        self._grid = defaultdict(set)
        self._bodies = set()
        self._dirty_bodies = set()
        self._collisions = set()
        self.listener = listener

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def dirty(self):
        return bool(self._dirty_bodies)

    @property
    def bodies(self):
        return iter(self._bodies)

    @property
    def collisions(self):
        return iter(self._collisions)

    def flush(self):
        for body in list(self._dirty_bodies):
            body._update_bounding_box()
            self._update_grid(body)
            self._update_collisions(body)
            self._dirty_bodies.remove(body)

    def _update_grid(self, body):
        grid_box = get_grid_box(body._bounding_box, self._cell_size)
        if grid_box != body._grid_box:
            old_grid_positions = set(generate_grid_positions(body._grid_box))
            new_grid_positions = set(generate_grid_positions(grid_box))
            for grid_position in old_grid_positions - new_grid_positions:
                self._grid[grid_position].remove(body)
            for grid_position in new_grid_positions - old_grid_positions:
                self._grid[grid_position].add(body)
            body._grid_box = grid_box

    def _update_collisions(self, body):
        bodies = set(body._collisions.iterkeys())
        for grid_position in generate_grid_positions(body._grid_box):
            bodies |= self._grid[grid_position]
        bodies -= self._dirty_bodies
        for other_body in bodies:
            collision = body._collisions.get(other_body)
            if body.intersects(other_body):
                if collision is None:
                    collision = Collision(body, other_body)
                    self._add_collision(collision)
                else:
                    self._update_collision(collision)
            else:
                if collision is not None:
                    self._remove_collision(collision)

    def _add_body(self, body):
        self._bodies.add(body)
        self._dirty_bodies.add(body)

    def _remove_body(self, body):
        for collision in list(body._collisions.itervalues()):
            self._remove_collision(collision)
        for grid_position in generate_grid_positions(body._grid_box):
            self._grid[grid_position].remove(body)
        body._grid_box = (0, 0), (0, 0)
        self._bodies.remove(body)
        self._dirty_bodies.discard(body)

    def _add_collision(self, collision):
        body_a, body_b = collision.bodies
        self._collisions.add(collision)
        body_a._collisions[body_b] = collision
        body_b._collisions[body_a] = collision
        if self.listener is not None:
            self.listener.on_collision_add(collision)

    def _update_collision(self, collision):
        if self.listener is not None:
            self.listener.on_collision_update(collision)

    def _remove_collision(self, collision):
        if self.listener is not None:
            self.listener.on_collision_remove(collision)
        body_a, body_b = collision.bodies
        del body_b._collisions[body_a]
        del body_a._collisions[body_b]
        self._collisions.remove(collision)
