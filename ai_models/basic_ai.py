# -*- coding: utf-8 -*-

# ai_models/basic_ai.py

MAX_HORIZONTAL_LANDING_SPEED = 5
MAX_VERTICAL_LANDING_SPEED = 5

class BasicAI_old:
    def __init__(self, lander, planet, target_descent_rate=-MAX_VERTICAL_LANDING_SPEED):
        self.lander = lander
        self.planet = planet
        self.target_descent_rate = target_descent_rate  # Target descent rate (m/s)
        
    def control(self):
        """AI control logic: returns desired thrust and angle."""
        lander_state = self.lander.get_state()
        
        # Simple logic: if descending too fast, increase thrust
        vertical_speed = lander_state['velocity'][1]
        
        if vertical_speed < self.target_descent_rate :
            thrust = 1.0   # Increase thrust
        else :
            thrust = 0.0   # Reduce thrust
        angle = 0  # For now, no tilt control (we’ll focus on vertical descent)
        
        self.lander.pilot_commands(thrust=thrust, angle=angle)
        return thrust, angle

# ai_models/basic_ai.py

from ai_models.dqn_ai import DQNAI
import numpy as np

def normalize(value, min_value, max_value):
    """Normalize value to the range [0, 1]."""
    return (value - min_value) / (max_value - min_value)
    
class BasicAI:
    def __init__(self, lander, planet):
        self.lander = lander
        self.planet = planet
        self.state_size = 4 + 5 + 2 + 2 + 1 + 1 + 5  # planet general info + lander general info + dx, dy, vx, vy, angle, fuel, terrain_info (assuming 5 rays)
        self.action_size = 2  # Thrust and angle change
        self.ai_model = DQNAI(lander, planet, self.state_size, self.action_size)
        self.landing_x_center, self.landing_y_center = None, None
        self.prepare_for_landing()
        

    def prepare_for_landing(self):
        # Estimate initial fuel
        self.estimate_initial_fuel()
        self.landing_x_center = (self.planet.landing_zone[0][0] + self.planet.landing_zone[1][0]) / 2
        self.landing_y_center = self.planet.landing_zone[0][1]
        
    def control(self):
        # Get the current state as a vector
        state = self.get_state_vector()
        # Get action from DQNAI model
        thrust, angle_change, thrust_idx, angle_idx = self.ai_model.act(state)
        # Apply the actions to the lander
        self.lander.pilot_commands(thrust=thrust, angle=self.lander.angle + angle_change)
        return thrust, angle_change, thrust_idx, angle_idx

    def estimate_initial_fuel(self):
        """
        Estimate and set the initial fuel quantity based on planet characteristics.
        """
        # For simplicity, we'll set fuel based on gravity and atmosphere thickness
        gravity = self.planet.gravity_constant
        atmosphere = self.planet.atmosphere_thickness

        # Simple heuristic: more gravity and thicker atmosphere require more fuel
        fuel_estimate = min(self.lander.max_fuel, gravity * atmosphere * 0.1)
        self.lander.adjust_fuel(fuel_estimate)
    
    def get_state_vector(self):
        # Convert lander state to a vector
        state = self.lander.get_state()
        position = state['position']
        velocity = state['velocity']
        angle = [state['angle']]
        fuel = [state['fuel']]
    
        # Distance to landing zone
        if abs(position[0] - self.landing_x_center) < abs(position[0] + self.planet.ground_length - self.landing_x_center) :    
            dx = [position[0] - self.landing_x_center]
        else:
            dx = [position[0] + self.planet.ground_length - self.landing_x_center]
        dy = [position[1] - self.landing_y_center]
    
        # Terrain sensing
        terrain_info = self.lander.sense_terrain(self.planet)
    
        # Planet properties (normalized)
        p1 = [normalize(self.planet.radius, 1000, 10000)]  # Normalize radius (example range: 1000 to 10000)
        p2 = [normalize(self.planet.atmosphere_thickness, 500, 1500)]  # Normalize atmosphere thickness
        p3 = [normalize(self.planet.air_ground_density, 0.5, 3.0)]  # Normalize air density
        p4 = [normalize(self.planet.gravity_constant, 1, 20)]  # Normalize gravity constant
    
        # Lander properties (normalized)
        l1 = [normalize(self.lander.max_thrust, 500, 5000)]  # Normalize max thrust
        l2 = [normalize(self.lander.max_fuel, 100, 1000)]  # Normalize max fuel
        l3 = [normalize(self.lander.drag_coeff, 0.2, 0.8)]  # Normalize drag coefficient
        l4 = [normalize(self.lander.surface_area, 1, 10)]  # Normalize surface area
        l5 = [normalize(self.lander.mass, 52.5, 525)]  # Normalize mass
    
        # Normalize dynamic state data
        dx = [(normalize(dx[0], -self.planet.ground_length / 2, self.planet.ground_length / 2)-0.5)*2]
        dy = [(normalize(dy[0], -self.planet.atmosphere_thickness, self.planet.atmosphere_thickness)-0.5)*2]  # Normalize height (example: max 2000 meters)
        velocity = [normalize(v, -500, 500) for v in velocity]  # Normalize velocities
        angle = [(normalize(angle[0], -180, 180)-0.5)*2]  # Normalize angle (-180 to 180 degrees)
        fuel = [normalize(fuel[0], 0, 100)]  # Normalize fuel
    
        # Combine all state information
        state_vector = np.concatenate([p1, p2, p3, p4,
                                       l1, l2, l3, l4, l5,
                                       dx, dy, velocity, angle, fuel, terrain_info])
        return state_vector
    
