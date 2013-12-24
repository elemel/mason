from app.block_entity import BlockEntity
from app.entity import Entity

class CharacterEntity(Entity):
    def __init__(self, controls, state_component, physics_component,
                 collision_world, collision_body, ground_sensor, batch, image,
                 sprite, size=(1.0, 1.0), facing=1):
        self.controls = controls
        self.state_component = state_component
        self.physics_component = physics_component
        self.collision_world = collision_world
        self.collision_body = collision_body
        self.ground_sensor = ground_sensor
        self.batch = batch
        self.image = image
        self.sprite = sprite
        self.size = size
        self.facing = facing 

    def create(self):
        self.collision_body.world = self.collision_world
        self.ground_sensor.world = self.collision_world
        self.sprite.batch = self.batch
        self.draw(0.5)
        self.physics_component.create()
        self.state_component.create()

    def delete(self):
        self.state_component.delete()
        self.physics_component.delete()
        self.sprite.batch = None
        self.ground_sensor.world = None
        self.collision_body.world = None

    def update(self, dt):
        self.controls.update(dt)
        self.physics_component.update(dt)
        self.update_collision_body(dt)
        self.update_ground_sensor(dt)

    def update_collision_body(self, dt):
        box = self.collision_body.shape
        x, y = self.physics_component.position
        width, height = self.size
        box.p1 = x - 0.5 * width, y - 0.5 * height
        box.p2 = x + 0.5 * width, y + 0.5 * height
        self.collision_body.touch()

    def update_ground_sensor(self, dt):
        box = self.ground_sensor.shape
        x, y = self.physics_component.position
        width, height = self.size
        box.p1 = x - 0.5 * width, y - 0.5 * height - 0.05
        box.p2 = x + 0.5 * width, y - 0.5 * height + 0.05
        self.ground_sensor.touch()

    def is_standing(self):
        return any(isinstance(body.user_data, BlockEntity)
                   for body in self.ground_sensor.collision_bodies)

    def draw(self, t):
        x, y = self.physics_component.position
        self.sprite.position = self.physics_component.position
