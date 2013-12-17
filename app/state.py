class State(object):
    def __init__(self):
        self._state_machine = None

    @property
    def state_machine(self):
        return self._state_machine

    def create(self):
        pass

    def delete(self):
        pass

class StateMachine(object):
    def __init__(self, state=None):
        self._state = None
        self._created = False
        self.state = state

    def create(self):
        if self._state is not None:
            self._state._state_machine = self
            self._state.create()
        self._created = True

    def delete(self):
        if self._state is not None:
            self._state.delete()
            self._state._state_machine = None
        self._created = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state is not self._state:
            if self._created and self._state is not None:
                self._state.delete()
                self._state._state_machine = None
            self._state = state
            if self._created and self._state is not None:
                self._state._state_machine = self
                self._state.create()
