from app.collision import CollisionListener

class GameCollisionListener(CollisionListener):
    def __init__(self):
        self.collisions = set()

    def on_collision_add(self, collision):
        self.collisions.add(collision)

    def on_collision_update(self, collision):
        self.collisions.add(collision)
