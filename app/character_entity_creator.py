from app.character_entity import CharacterEntity
from app.character_states import CharacterStandState
from app.collision import CollisionBody, CollisionBox
from app.controls import KeyControls
from app.physics_component import PhysicsComponent
from app.state import StateMachine
from app.state_component import StateComponent
from app.subpixel_sprite import SubpixelSprite

import pyglet

class CharacterEntityCreator(object):
    def __init__(self, key_state_handler, state_update_phase,
                 collision_detector, batch):
        self.key_state_handler = key_state_handler
        self.state_update_phase = state_update_phase
        self.collision_detector = collision_detector
        self.batch = batch
        self.image = pyglet.resource.image('images/mario.png')

    def create(self, position=(0.0, 0.0), size=(1.0, 1.0)):
        controls = KeyControls(self.key_state_handler)
        physics_component = PhysicsComponent(
            position=position,
            max_velocity=10.0,
        )
        state = CharacterStandState(
            controls,
            physics_component,
            self.state_update_phase,
        )
        state_machine = StateMachine(state)
        state_component = StateComponent(state_machine)
        x, y = position
        width, height = size
        x1 = x - 0.5 * width
        y1 = x - 0.5 * height
        x2 = x + 0.5 * width
        y2 = x + 0.5 * height
        p1 = x1, y1
        p2 = x2, y2
        collision_shape = CollisionBox(p1, p2)
        collision_body = CollisionBody(collision_shape)
        sprite = SubpixelSprite(self.image)
        sprite.scale = 1.0 / float(self.image.width)
        entity = CharacterEntity(
            controls=controls,
            state_component=state_component,
            physics_component=physics_component,
            collision_detector=self.collision_detector,
            collision_body=collision_body,
            batch=self.batch,
            sprite=sprite,
            size=size,
        )
        collision_body.user_data = entity
        return entity
