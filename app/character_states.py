from app.state import State
from app.update import UpdateHandler

class CharacterStateFactory(object):
    def __init__(self, entity, controls, physics_component, update_phase):
        self.entity = entity
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase

    def create_fall_state(self):
        return CharacterFallState(
            entity=self.entity,
            controls=self.controls,
            physics_component=self.physics_component,
            update_phase=self.update_phase,
            state_factory=self,
        )

    def create_jump_state(self):
        return CharacterJumpState(
            entity=self.entity,
            physics_component=self.physics_component,
            update_phase=self.update_phase,
            state_factory=self,
        )

    def create_stand_state(self):
        return CharacterStandState(
            entity=self.entity,
            controls=self.controls,
            physics_component=self.physics_component,
            update_phase=self.update_phase,
            state_factory=self,
        )

    def create_walk_state(self):
        return CharacterWalkState(
            entity=self.entity,
            controls=self.controls,
            physics_component=self.physics_component,
            update_phase=self.update_phase,
            state_factory=self,
        )

class CharacterFallState(State, UpdateHandler):
    def __init__(self, entity, controls, physics_component, update_phase,
                 state_factory):
        self.entity = entity
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.state_factory = state_factory

    def create(self):
        self.physics_component.acceleration = 0.0, -10.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)

    def update(self, dt):
        if self.entity.is_standing():
            self.state_machine.state = self.state_factory.create_stand_state()
            return

class CharacterJumpState(State, UpdateHandler):
    def __init__(self, entity, physics_component, update_phase, state_factory):
        self.entity = entity
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.state_factory = state_factory

    def create(self):
        velocity_x, velocity_y = self.physics_component.velocity
        self.physics_component.velocity = velocity_x, 6.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)

    def update(self, dt):
        self.state_machine.state = self.state_factory.create_fall_state()

class CharacterStandState(State, UpdateHandler):
    def __init__(self, entity, controls, physics_component, update_phase,
                 state_factory):
        self.entity = entity
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.state_factory = state_factory

    def create(self):
        self.physics_component.acceleration = 0.0, -10.0
        self.physics_component.friction = 10.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)
        self.physics_component.friction = 0.0

    def update(self, dt):
        if not self.entity.is_standing():
            self.state_machine.state = self.state_factory.create_fall_state()
            return
        if self.controls.up:
            self.state_machine.state = self.state_factory.create_jump_state()
            return
        if self.controls.x:
            self.state_machine.state = self.state_factory.create_walk_state()
            return

class CharacterWalkState(State, UpdateHandler):
    def __init__(self, entity, controls, physics_component, update_phase,
                 state_factory):
        self.entity = entity
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.state_factory = state_factory

    def create(self):
        self.physics_component.acceleration = 0.0, -10.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)
        self.physics_component.acceleration = 0.0, -10.0

    def update(self, dt):
        if not self.controls.x:
            self.state_machine.state = self.state_factory.create_stand_state()
            return

        acceleration_x = 10.0 * float(self.controls.x)
        self.physics_component.acceleration = acceleration_x, -10.0
