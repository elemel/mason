import pyglet

class Controls(object):
    def __init__(self):
        self.x = 0.0
        self.z = 0.0

    def update(self, dt):
        pass

class KeyControls(Controls):
    def __init__(self, key_state_handler):
        super(KeyControls, self).__init__()
        self.key_state_handler = key_state_handler

    def update(self, dt):
        left = self.key_state_handler[pyglet.window.key.LEFT]
        right = self.key_state_handler[pyglet.window.key.RIGHT]
        up = self.key_state_handler[pyglet.window.key.UP]
        down = self.key_state_handler[pyglet.window.key.DOWN]
        self.x = float(right) - float(left)
        self.z = float(up) - float(down)
