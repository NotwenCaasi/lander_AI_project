# -*- coding: utf-8 -*-
# Contains lander dynamics and aero properties
# Lander dynamics and state updates

# lander/lander.py

import numpy as np
import math

from environments.physics import get_terrain_height_at_x

class Lander:
    def __init__(self, max_thrust, max_fuel, drag_coeff, mass, surface_area):
        self.max_thrust = max_thrust  # Max thrust (N)
        self.max_fuel = max_fuel # max fuel 
        self.thrust = 0.0 # 0-1 of max_thrust
        self.drag_coeff = drag_coeff  # Drag coefficient (dimensionless)
        self.mass = mass  # Mass of the lander (kg)
        self.surface_area = surface_area  # Surface area (m^2)
        self.position = np.array([0.0, 0.0])  # Position (x, y)
        self.velocity = np.array([0.0, 0.0])  # Velocity (vx, vy)
        self.angle = 0.0  # Orientation (angle in degrees)
        self.fuel = 100.0  # Fuel remaining (percentage)
        self.is_landed = False
        self.crashed = False  # Reset crash status
        self.last_terrain_idx = 0

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
            dt = min(0.2, max(-0.2, dt))
            thrust = self.thrust + dt
            thrust = min(1.0, max(0.0, thrust))
            self.thrust = thrust            
        if self.fuel <= 0:
            self.thrust = 0
        if angle is not None:
            da = angle - self.angle
            da = min(15, max(-15, da))
            angle = self.angle + da
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
        self.crashed = False  # Reset crash status
    
    def adjust_fuel(self, fuel_quantity):
        """
        Adjust the initial fuel quantity at atmosphere entry.
        """
        self.fuel = min(fuel_quantity, self.max_fuel)
    
    def sense_terrain(self, planet, num_rays=5, max_distance=1000):
        """
        Simulate terrain sensing with ray casting.
        Returns an array of distances to obstacles in specified directions.
        """
        angles = np.linspace(-np.pi/2, np.pi/2, num_rays)  # Rays from -90 to +90 degrees relative to lander
        distances = []
    
        for angle in angles:
            distance = self.cast_ray(planet, angle, max_distance)
            distances.append(distance)
        
        return distances
    
    def cast_ray(self, planet, angle, max_distance):
        """
        Cast a ray from the lander's current position at a given angle.
        Returns the distance to the first obstacle within max_distance.
        """
        x0, y0 = self.position
        angle += np.deg2rad(self.angle)  # Adjust for lander's orientation
        for d in np.linspace(0, max_distance, num=100):
            x = x0 + d * np.cos(angle)
            y = y0 + d * np.sin(angle)
            terrain_height = get_terrain_height_at_x(self, planet.terrain)
            if y <= terrain_height:
                return d  # Obstacle detected
        return max_distance  # No obstacle within max_distance
