from app.component import Component
from app.maths import sign

from math import sqrt

class PhysicsComponent(Component):
    def __init__(self, position=(0.0, 0.0), velocity=(0.0, 0.0),
                 max_velocity=1.0, acceleration=(0.0, 0.0), friction=0.0):
        self.position = position
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.friction = friction

    def update(self, dt):
        x, y = self.position
        velocity_x, velocity_y = self.velocity
        max_velocity = max(self.max_velocity,
                           sqrt(velocity_x ** 2 + velocity_y ** 2))
        acceleration_x, acceleration_y = self.acceleration

        # Apply acceleration
        velocity_x += acceleration_x * dt
        velocity_y += acceleration_y * dt

        # Calculate direction
        direction_x = 0.0
        direction_y = 0.0
        velocity_length = sqrt(velocity_x ** 2 + velocity_y ** 2)
        if velocity_length > 0.0:
            direction_x = velocity_x / velocity_length
            direction_y = velocity_y / velocity_length

        # Apply friction
        if self.friction > 0.0:
            velocity_x = (sign(velocity_x) *
                          max(0.0, abs(velocity_x -
                                       self.friction * direction_x * dt)))
            velocity_y = (sign(velocity_y) *
                          max(0.0, abs(velocity_y -
                                       self.friction * direction_y * dt)))

        # Apply max velocity
        if velocity_x ** 2 + velocity_y ** 2 > max_velocity ** 2:
            velocity_length = sqrt(velocity_x ** 2 + velocity_y ** 2)
            velocity_x = max_velocity * velocity_x / velocity_length
            velocity_y = max_velocity * velocity_y / velocity_length

        # Apply velocity
        x += velocity_x * dt
        y += velocity_y * dt

        self.position = x, y
        self.velocity = velocity_x, velocity_y
