import pyglet

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super(GameWindow, self).__init__(caption='MASON')
        self._view = None

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, view):
        if self._view is not None:
            self._view.delete()
        self._view = view
        if self._view is not None:
            self._view.create()

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.ESCAPE:
            self.close()
        elif self._view is not None:
            self._view.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        if self._view is not None:
            self._view.on_key_release(key, modifiers)

    def on_draw(self):
        if self._view is not None:
            self._view.on_draw()
