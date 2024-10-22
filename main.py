# -*- coding: utf-8 -*-
# Main script to run the simulation and train AI

# main.py

import argparse
import random

from lander.lander import Lander
from environments.planet import Planet
from ai_models.basic_ai import BasicAI
from utils.animation import Animation

FUEL_DENSITY = 0.1
    
def main():
    # Argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Lander simulation")
    parser.add_argument('--display', action='store_true', help="Enable display for animation")
    
    args = parser.parse_args()

    # Define planet properties
    # radius = random.randint(1000, 10000)
    # atmosphere_thickness = random.randint(int(radius/20), int(radius/5))
    # air_ground_density = random.randint(0,50)/10
    # gravity_constant = random.randint(30, 200)/10
    
    radius = 6000
    atmosphere_thickness = 1000
    air_ground_density = 1.0
    gravity_constant = 9.8
    planet = Planet(
        radius=radius,
        atmosphere_thickness=atmosphere_thickness,
        air_ground_density=air_ground_density,
        gravity_constant=gravity_constant)

    # Define lander properties
    max_thrust = 2000
    max_fuel = 100
    drag_coeff = 0.5
    surface_area = 4.0
    
    
    mass = max_fuel*FUEL_DENSITY+max_thrust/200
    
    lander = Lander(
        max_thrust=max_thrust, max_fuel=max_fuel,
        drag_coeff=drag_coeff, mass=mass, surface_area=surface_area)

    # Set initial position for the lander
    x0 = float(random.randint(0, int(planet.ground_length)))
    y0 = float(planet.atmosphere_thickness)
    v0 = float(random.randint(0,100))
    a0 = random.randint(-90, 90)
    t0 = 0
    start_position = (x0, y0, v0, a0, t0)  # Start at x=5000, altitude=800, speed = 0, angle=0, thrust=0

    # Create basic AI model
    ai_model = BasicAI(lander, target_descent_rate=-5)

    # Create the Animation object without display
    animation = Animation(lander, ai_model, planet, start_position,
                          total_time=100.0, display=args.display)

    # Run the simulation (no display)
    animation.run()


if __name__ == "__main__":
    main()