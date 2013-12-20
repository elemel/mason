from app.camera import Camera
from app.collision import CollisionListener, CollisionWorld
from app.block_entity_creator import BlockEntityCreator
from app.block_grid import BlockGrid
from app.character_entity_creator import CharacterEntityCreator
from app.entity_manager import EntityManager
from app.game_collision_listener import GameCollisionListener
from app.game_view import GameView
from app.game_window import GameWindow
from app.scene import Scene
from app.update import UpdateManager, UpdatePhase

import pyglet
import random

def open_joysticks():
    joysticks = pyglet.input.get_joysticks()[:4]
    for joystick in joysticks:
        joystick.open()
    joysticks += [None] * (4 - len(joysticks))
    return joysticks

def main():
    pyglet.resource.path.append('../data')
    pyglet.resource.reindex()

    entity_manager = EntityManager()
    block_grid = BlockGrid()

    state_update_phase = UpdatePhase()
    update_phases = [state_update_phase]
    update_manager = UpdateManager(update_phases)

    scene = Scene()
    camera = Camera(scale=5.0)
    game_window = GameWindow()
    collision_listener = GameCollisionListener()
    collision_world = CollisionWorld(listener=collision_listener)
    batch = pyglet.graphics.Batch()
    key_state_handler = pyglet.window.key.KeyStateHandler()
    joysticks = open_joysticks()
    block_entity_creator = BlockEntityCreator(collision_world, batch)
    character_entity_creator = CharacterEntityCreator(key_state_handler,
                                                      joysticks,
                                                      state_update_phase,
                                                      collision_world,
                                                      batch,
                                                      block_entity_creator,
                                                      entity_manager,
                                                      block_grid)
    game_view = GameView(game_window, batch, key_state_handler,
                         entity_manager, update_manager, collision_world,
                         collision_listener, camera)
    game_window.view = game_view
    for i in xrange(-1, 2):
        position = float(i), 0.0
        block_entity = block_entity_creator.create(position=position)
        game_view.add_entity(block_entity)
    character_entity = character_entity_creator.create(position=(0.0, 2.0))
    game_view.add_entity(character_entity)
    pyglet.app.run()

if __name__ == '__main__':
    main()
