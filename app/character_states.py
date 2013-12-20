from app.maths import clamp
from app.state import State
from app.update import UpdateHandler

from math import floor

class CharacterStateFactory(object):
    def __init__(self, entity, controls, physics_component, update_phase,
                 block_entity_creator, entity_manager, block_grid):
        self.entity = entity
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.block_entity_creator = block_entity_creator
        self.entity_manager = entity_manager
        self.block_grid = block_grid

    def create_build_down_state(self):
        return CharacterBuildState(
            grid_direction_y=-1,
            physics_component=self.physics_component,
            update_phase=self.update_phase,
            state_factory=self,
            block_entity_creator=self.block_entity_creator,
            entity_manager=self.entity_manager,
            block_grid=self.block_grid,
        )

    def create_build_up_state(self):
        return CharacterBuildState(
            grid_direction_y=1,
            physics_component=self.physics_component,
            update_phase=self.update_phase,
            state_factory=self,
            block_entity_creator=self.block_entity_creator,
            entity_manager=self.entity_manager,
            block_grid=self.block_grid,
        )

    def create_crouch_state(self):
        return CharacterCrouchState(
            entity=self.entity,
            controls=self.controls,
            update_phase=self.update_phase,
            state_factory=self,
        )

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

class CharacterBuildState(State, UpdateHandler):
    def __init__(self, grid_direction_y, physics_component, update_phase,
                 state_factory, block_entity_creator, entity_manager,
                 block_grid):
        self.grid_direction_y = grid_direction_y
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.state_factory = state_factory
        self.block_entity_creator = block_entity_creator
        self.entity_manager = entity_manager
        self.block_grid = block_grid

    def create(self):
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)

    def update(self, dt):
        x, y = self.physics_component.position
        grid_x, grid_y = int(floor(x)) + 1, int(floor(y)) - 1
        if self.block_grid[grid_x, grid_y] is not None:
            grid_x += 1
        if self.block_grid[grid_x, grid_y] is not None:
            grid_y += 1
        if self.block_grid[grid_x, grid_y] is None:
            block_position = float(grid_x), float(grid_y)
            block_entity = self.block_entity_creator.create(
                position=block_position)
            self.entity_manager.add_entity(block_entity)
            self.block_grid[grid_x, grid_y] = block_entity
        self.state_machine.state = self.state_factory.create_crouch_state()

    def _get_build_grid_position(self):
        if self.grid_direction_y == -1:
            return self._get_build_down_grid_position()
        else:
            return self._get_build_up_grid_position()

class CharacterCrouchState(State, UpdateHandler):
    def __init__(self, entity, controls, update_phase, state_factory):
        self.entity = entity
        self.controls = controls
        self.update_phase = update_phase
        self.state_factory = state_factory

    def create(self):
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)

    def update(self, dt):
        if not self.entity.is_standing():
            self.state_machine.state = self.state_factory.create_fall_state()
            return
        if not self.controls.y:
            self.state_machine.state = self.state_factory.create_stand_state()
            return

class CharacterFallState(State, UpdateHandler):
    def __init__(self, entity, controls, physics_component, update_phase,
                 state_factory):
        self.entity = entity
        self.controls = controls
        self.physics_component = physics_component
        self.update_phase = update_phase
        self.state_factory = state_factory
        self.drift_acceleration = 10.0
        self.drift_velocity = 2.0

    def create(self):
        self.physics_component.acceleration = 0.0, -10.0
        self.update_phase.add_handler(self)

    def delete(self):
        self.update_phase.remove_handler(self)

    def update(self, dt):
        if self.entity.is_standing():
            self.state_machine.state = self.state_factory.create_stand_state()
            return
        if self.controls.x:
            control_x = float(self.controls.x)
            velocity_x, velocity_y = self.physics_component.velocity
            min_velocity = min(velocity_x, -self.drift_velocity)
            max_velocity = max(velocity_x, self.drift_velocity)
            velocity_x += dt * control_x * self.drift_acceleration
            velocity_x = clamp(velocity_x, min_velocity, max_velocity)
            self.physics_component.velocity = velocity_x, velocity_y

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
        if self.controls.jump:
            self.state_machine.state = self.state_factory.create_jump_state()
            return
        if self.controls.x:
            self.state_machine.state = self.state_factory.create_walk_state()
            return
        if self.controls.y == -1:
            self.state_machine.state = \
                    self.state_factory.create_build_down_state()
            return
        if self.controls.y == 1:
            self.state_machine.state = \
                    self.state_factory.create_build_up_state()
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
        if not self.entity.is_standing():
            self.state_machine.state = self.state_factory.create_fall_state()
            return
        if self.controls.jump:
            self.state_machine.state = self.state_factory.create_jump_state()
            return
        if not self.controls.x:
            self.state_machine.state = self.state_factory.create_stand_state()
            return

        acceleration_x = 10.0 * float(self.controls.x)
        self.physics_component.acceleration = acceleration_x, -10.0
