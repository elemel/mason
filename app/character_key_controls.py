from pyglet.window import key

class CharacterKeyControls(object):
    def __init__(self, key_state_handler):
        self.key_state_handler = key_state_handler
        self.move = 0.0, 0.0

    def update(self, dt):
        up = self.key_state_handler[key.UP]
        left = self.key_state_handler[key.LEFT]
        down = self.key_state_handler[key.DOWN]
        right = self.key_state_handler[key.RIGHT]
        x = float(right) - float(left)
        y = float(up) - float(down)
        self.move = x, y
