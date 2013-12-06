import pyglet

class Controls(object):
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    @property
    def x(self):
        return int(self.right) - int(self.left)

    @property
    def y(self):
        return int(self.up) - int(self.down)

    def update(self, dt):
        pass

class KeyControls(Controls):
    def __init__(self, key_state_handler):
        super(KeyControls, self).__init__()
        self.key_state_handler = key_state_handler

    def update(self, dt):
        self.left = self.key_state_handler[pyglet.window.key.LEFT]
        self.right = self.key_state_handler[pyglet.window.key.RIGHT]
        self.up = self.key_state_handler[pyglet.window.key.UP]
        self.down = self.key_state_handler[pyglet.window.key.DOWN]
