class EntityManager(object):
    def __init__(self):
        self.entities = set()

    def add_entity(self, entity):
        self.entities.add(entity)
        entity.create()

    def remove_entity(self, entity):
        entity.delete()
        self.entities.remove(entity)
