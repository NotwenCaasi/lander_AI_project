# -*- coding: utf-8 -*-
# Main script to run the simulation and train AI

# main.py

import argparse
from lander.lander import Lander
from environments.planet import Planet
from ai_models.basic_ai import BasicAI
from utils.animation import Animation

from utils.animation import Animation

def main():
    # Argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Lander simulation")
    parser.add_argument('--display', action='store_true', help="Enable display for animation")
    
    args = parser.parse_args()

    # Define planet properties
    planet = Planet(radius=6000, atmosphere_thickness=1000, gravity_constant=9.8)

    # Define lander properties
    lander = Lander(max_thrust=1500, max_fuel=100, drag_coeff=0.5, mass=1000, surface_area=4.0)

    # Set initial position for the lander
    start_position = (5000.0, 800.0, 0, 0, 0)  # Start at x=5000, altitude=800, speed = 0, angle=0, thrust=0

    # Create basic AI model
    ai_model = BasicAI(lander, target_descent_rate=-5)

    # Create the Animation object without display
    animation = Animation(lander, ai_model, planet, start_position, total_time=1.0, display=args.display)

    # Run the simulation (no display)
    animation.run()


if __name__ == "__main__":
    main()