from app.component import Component

class StateComponent(Component):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def create(self):
        self.state_machine.create()

    def delete(self):
        self.state_machine.delete()
