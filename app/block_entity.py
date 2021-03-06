from app.entity import Entity

import pyglet

class BlockEntity(Entity):
    def __init__(self, collision_world, collision_body, batch, sprite,
                 position=(0.0, 0.0), size=(1.0, 1.0)):
        self.collision_world = collision_world
        self.collision_body = collision_body
        self.batch = batch
        self.sprite = sprite
        self.position = position
        self.size = size

    def create(self):
        self.collision_body.world = self.collision_world
        self.sprite.batch = self.batch
        self.draw(0.5)

    def delete(self):
        self.sprite.batch = None
        self.collision_body.world = None

    def draw(self, t):
        x, y = self.position
        width, height = self.size
        self.sprite.position = x - 0.5 * width, y - 0.5 * height
