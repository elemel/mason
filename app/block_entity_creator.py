from app.block_entity import BlockEntity
from app.collision import CollisionBody, CollisionBox
from app.subpixel_sprite import SubpixelSprite

import pyglet

class BlockEntityCreator(object):
    def __init__(self, collision_world, batch):
        self.collision_world = collision_world
        self.batch = batch
        self.image = pyglet.resource.image('images/block.png')

    def create(self, position=(0.0, 0.0), size=(1.0, 1.0)):
        x, y = position
        width, height = size
        x1 = x - 0.5 * width
        y1 = y - 0.5 * height
        x2 = x + 0.5 * width
        y2 = y + 0.5 * height
        p1 = x1, y1
        p2 = x2, y2
        collision_shape = CollisionBox(p1, p2)
        collision_body = CollisionBody(collision_shape)
        sprite = SubpixelSprite(self.image)
        sprite.scale = 1.0 / float(self.image.width)
        entity = BlockEntity(
            collision_world=self.collision_world,
            collision_body=collision_body,
            batch=self.batch,
            sprite=sprite,
            position=position,
            size=size,
        )
        collision_body.user_data = entity
        return entity
