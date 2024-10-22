# -*- coding: utf-8 -*-

# ai_models/basic_ai.py

MAX_HORIZONTAL_LANDING_SPEED = 5
MAX_VERTICAL_LANDING_SPEED = 5

class BasicAI:
    def __init__(self, lander, target_descent_rate=-MAX_VERTICAL_LANDING_SPEED):
        self.lander = lander
        self.target_descent_rate = target_descent_rate  # Target descent rate (m/s)
        
    def control(self):
        """AI control logic: returns desired thrust and angle."""
        lander_state = self.lander.get_state()
        
        # Simple logic: if descending too fast, increase thrust
        vertical_speed = lander_state['velocity'][1]
        
        if vertical_speed < self.target_descent_rate :
            thrust = 0.8   # Increase thrust
        elif vertical_speed > 0 :
            thrust = 0.0
        else :
            thrust = 0.2   # Reduce thrust
        angle = 0  # For now, no tilt control (we’ll focus on vertical descent)
        
        self.lander.pilot_commands(thrust=thrust, angle=angle)
        return thrust, angle

