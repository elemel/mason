import pyglet

class Controls(object):
    def __init__(self):
        self.up = False
        self.left = False
        self.down = False
        self.right = False

        self.jump = False
        self.run = False

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
        self.up = self.key_state_handler[pyglet.window.key.W]
        self.left = self.key_state_handler[pyglet.window.key.A]
        self.down = self.key_state_handler[pyglet.window.key.S]
        self.right = self.key_state_handler[pyglet.window.key.D]

        self.jump = self.key_state_handler[pyglet.window.key.SPACE]
        self.run = self.key_state_handler[pyglet.window.key.LSHIFT]
