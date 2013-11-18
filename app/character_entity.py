from app.entity import Entity

class CharacterEntity(Entity):
    def __init__(self, controls, physics_component, collision_detector,
                 collision_body, batch, sprite, size=(1.0, 1.0)):
        self.controls = controls
        self.physics_component = physics_component
        self.collision_detector = collision_detector
        self.collision_body = collision_body
        self.batch = batch
        self.sprite = sprite
        self.size = size

    def create(self):
        self.collision_body.detector = self.collision_detector
        self.sprite.batch = self.batch
        self.draw(0.5)

    def delete(self):
        self.sprite.batch = None
        self.collision_body.detector = None

    def update(self, dt):
        self.controls.update(dt)
        move_x, move_y = self.controls.move
        self.physics_component.acceleration = move_x, -10.0
        self.physics_component.update(dt)
        self.update_collision_body(dt)

    def update_collision_body(self, dt):
        box = self.collision_body.shape
        x, y = self.physics_component.position
        box.p1 = x - 0.5, y - 0.5
        box.p2 = x + 0.5, y + 0.5
        self.collision_body.touch()

    def draw(self, t):
        x, y = self.physics_component.position
        width, height = self.size
        self.sprite.position = x - 0.5 * width, y - 0.5 * height
