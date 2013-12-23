from app.character_entity import CharacterEntity
from app.character_states import CharacterStateFactory
from app.collision import CollisionBody, CollisionBox
from app.controls import KeyControls, WiimoteControls
from app.physics_component import PhysicsComponent
from app.state import StateMachine
from app.state_component import StateComponent
from app.subpixel_sprite import SubpixelSprite

import pyglet

class CharacterEntityCreator(object):
    def __init__(self, key_state_handler, joysticks, state_update_phase,
                 collision_world, batch, block_entity_creator, entity_manager,
                 block_grid):
        self.key_state_handler = key_state_handler
        self.joysticks = list(joysticks)
        self.state_update_phase = state_update_phase
        self.collision_world = collision_world
        self.batch = batch
        self.image = pyglet.resource.image('images/mario.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.block_entity_creator = block_entity_creator
        self.entity_manager = entity_manager
        self.block_grid = block_grid

    def create(self, position=(0.0, 0.0), size=(1.0, 1.0), facing=1):
        if self.joysticks[0] is None:
            controls = KeyControls(self.key_state_handler)
        else:
            controls = WiimoteControls(self.joysticks[0])
        physics_component = PhysicsComponent(
            position=position,
            max_velocity=10.0,
        )
        state_machine = StateMachine()
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
        ground_sensor_p1 = x - 0.5, y - 0.6
        ground_sensor_p2 = x + 0.5, y - 0.4
        ground_sensor_shape = CollisionBox(ground_sensor_p1, ground_sensor_p2)
        ground_sensor = CollisionBody(ground_sensor_shape)
        sprite = SubpixelSprite(self.image)
        sprite.scale = 1.0 / float(self.image.width)
        entity = CharacterEntity(
            controls=controls,
            state_component=state_component,
            physics_component=physics_component,
            collision_world=self.collision_world,
            collision_body=collision_body,
            ground_sensor=ground_sensor,
            batch=self.batch,
            image=self.image,
            sprite=sprite,
            size=size,
            facing=1,
        )
        collision_body.user_data = entity
        state_factory = CharacterStateFactory(
            entity=entity,
            controls=controls,
            physics_component=physics_component,
            update_phase=self.state_update_phase,
            block_entity_creator=self.block_entity_creator,
            entity_manager=self.entity_manager,
            block_grid=self.block_grid,
        )
        state_machine.state = state_factory.create_stand_state()
        return entity
