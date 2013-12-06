class UpdateHandler(object):
    def update(self, dt):
        pass

class UpdatePhase(object):
    def __init__(self):
        self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)

    def remove_handler(self, handler):
        self.handlers.remove(handler)

    def update(self, dt):
        for handler in list(self.handlers):
            if handler in self.handlers:
                handler.update(dt)

class UpdateManager(object):
    def __init__(self, phases):
        self.phases = list(phases)

    def update(self, dt):
        for phase in self.phases:
            phase.update(dt)
