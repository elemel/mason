from app.block_entity import BlockEntity
from app.character_entity import CharacterEntity
from app.camera import Camera
from app.view import View

import pyglet
from pyglet.gl import *

class GameView(View):
    def __init__(self, window, batch, key_state_handler, entity_manager,
                 update_manager, collision_world, collision_listener, camera,
                 fixed_dt=(1.0 / 60.0), max_dt=1.0):
        self.window = window
        self.batch = batch
        self.key_state_handler = key_state_handler
        self.entity_manager = entity_manager
        self.update_manager = update_manager
        self.collision_world = collision_world
        self.collision_listener = collision_listener
        self.camera = camera
        self.fixed_dt = fixed_dt
        self.max_dt = max_dt
        self.dt = 0.0

    def create(self):
        pyglet.clock.schedule(self.update)

    def delete(self):
        pyglet.clock.unschedule(self.update)

    def add_entity(self, entity):
        self.entity_manager.add_entity(entity)

    def remove_entity(self, entity):
        self.entity_manager.remove_entity(entity)

    def on_key_press(self, key, modifiers):
        self.key_state_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.key_state_handler.on_key_release(key, modifiers)

    def update(self, dt):
        dt = min(dt, self.max_dt)
        self.dt += dt
        while self.fixed_dt < self.dt:
            self.update_manager.update(self.fixed_dt)
            for entity in self.entity_manager.entities:
                entity.update(self.fixed_dt)
            self.handle_collisions()
            self.dt -= self.fixed_dt

    def handle_collisions(self):
        self.collision_world.flush()
        for collision in self.collision_world.collisions:
            entity_a = collision.body_a.user_data
            entity_b = collision.body_b.user_data
            entity_types = type(entity_a), type(entity_b) 
            if entity_types == (BlockEntity, CharacterEntity):
                pass # self.handle_block_character_collision(entity_a, entity_b)
            if entity_types == (CharacterEntity, BlockEntity):
                self.handle_block_character_collision(entity_b, entity_a)

    def handle_block_character_collision(self, block_entity, character_entity):
        character_x, character_y = character_entity.physics_component.position
        block_x, block_y = block_entity.position
        character_y = block_y + 1.0
        character_entity.physics_component.position = character_x, character_y

        velocity_x, velocity_y = character_entity.physics_component.velocity
        velocity_y = 0.0
        character_entity.physics_component.velocity = velocity_x, velocity_y

    def on_draw(self):
        self.window.clear()

        camera_x, camera_y = self.camera.position
        camera_scale = self.camera.scale
        window_width = float(self.window.width)
        window_height = float(self.window.height)
        aspect_ratio = window_width / window_height

        camera_x1 = camera_x - aspect_ratio * camera_scale
        camera_x2 = camera_x + aspect_ratio * camera_scale
        camera_y1 = camera_y - camera_scale
        camera_y2 = camera_y + camera_scale

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(camera_x1, camera_x2, camera_y1, camera_y2, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

        for entity in self.entity_manager.entities:
            entity.draw(0.5)
        self.batch.draw()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, window_width, 0.0, window_height, -1.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
