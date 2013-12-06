from app.state import State
from app.update import UpdateHandler

class CharacterStandState(State, UpdateHandler):
    def __init__(self, controls, physics_component, update_phase):
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase

    def create(self):
        self.physics_component.acceleration = 0.0, -10.0
        self.physics_component.friction = 10.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)
        self.physics_component.friction = 0.0

    def update(self, dt):
        if self.controls.x:
            self.state_machine.state = CharacterWalkState(
                controls=self.controls,
                physics_component=self.physics_component,
                update_phase=self.update_phase,
            )
            return

class CharacterWalkState(State, UpdateHandler):
    def __init__(self, controls, physics_component, update_phase):
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase

    def create(self):
        self.physics_component.acceleration = 0.0, -10.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)
        self.physics_component.acceleration = 0.0, -10.0

    def update(self, dt):
        if not self.controls.x:
            self.state_machine.state = CharacterStandState(
                controls=self.controls,
                physics_component=self.physics_component,
                update_phase=self.update_phase,
            )
            return

        acceleration_x = 10.0 * float(self.controls.x)
        self.physics_component.acceleration = acceleration_x, -10.0
