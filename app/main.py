from app.camera import Camera
from app.collision import CollisionDetector, CollisionListener
from app.block_entity_creator import BlockEntityCreator
from app.character_entity_creator import CharacterEntityCreator
from app.game_collision_listener import GameCollisionListener
from app.game_view import GameView
from app.game_window import GameWindow
from app.scene import Scene

import pyglet
import random

def main():
    pyglet.resource.path.append('../data')
    pyglet.resource.reindex()

    scene = Scene()
    camera = Camera(scale=5.0)
    game_window = GameWindow()
    collision_listener = GameCollisionListener()
    collision_detector = CollisionDetector(listener=collision_listener)
    batch = pyglet.graphics.Batch()
    key_state_handler = pyglet.window.key.KeyStateHandler()
    block_entity_creator = BlockEntityCreator(collision_detector, batch)
    character_entity_creator = CharacterEntityCreator(key_state_handler,
                                                      collision_detector,
                                                      batch)
    game_view = GameView(game_window, batch, key_state_handler,
                         collision_detector, collision_listener, camera)
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
