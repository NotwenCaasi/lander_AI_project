# -*- coding: utf-8 -*-
# Contains lander dynamics and aero properties
# Lander dynamics and state updates

# import logging
# logging.basicConfig(level=logging.INFO)

# class Lander:
#     def update(self, thrust, angle_change, gravity, air_density):
#         # Log state updates
#         logging.info(f"Updating lander: thrust={thrust}, angle_change={angle_change}")

# lander/lander.py

import numpy as np
import math

class Lander:
    def __init__(self, max_thrust, max_fuel, drag_coeff, mass, surface_area):
        self.max_thrust = max_thrust  # Max thrust (N)
        self.max_fuel = max_fuel # max fuel 
        self.thrust = 0 # 0-100 of max_thrust
        self.drag_coeff = drag_coeff  # Drag coefficient (dimensionless)
        self.mass = mass  # Mass of the lander (kg)
        self.surface_area = surface_area  # Surface area (m^2)
        self.position = np.array([0.0, 0.0])  # Position (x, y)
        self.velocity = np.array([0.0, 0.0])  # Velocity (vx, vy)
        self.angle = 0.0  # Orientation (angle in degrees)
        self.fuel = 100.0  # Fuel remaining (percentage)
        self.is_landed = False

    def get_state(self):
        """Return the current state of the lander."""
        return {
            'position': self.position,
            'velocity': self.velocity,
            'angle': self.angle,
            'fuel': self.fuel,
            'thrust': self.thrust
        }

    def pilot_commands(self, thrust=None, angle=None):
        if thrust is not None:
            dt = thrust - self.thrust
            dt = min(20, max(-20, dt))
            thrust += dt
            thrust = min(100, max(0, thrust))
            self.thrust = thrust            
        if angle is not None:
            da = angle - self.angle
            da = min(15, max(-15, da))
            angle += da
            angle = min(100, max(0, angle))
            self.angle = angle
        return 0
    
    def reset(self, start_position):
        """Reset the lander to its initial conditions."""
        x, y, v, t, a = start_position
        self.position = np.array([x, y])
        self.velocity = np.array([v*math.sin(a*3.14/180), -v*math.cos(a*3.14/180)])
        self.angle = a
        self.fuel = 100.0
        self.thrust = t
        self.is_landed = False
