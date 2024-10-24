# -*- coding: utf-8 -*-
# Main script to run the simulation and train AI

# main.py

import argparse
import random
import logging

from lander.lander import Lander
from environments.planet import Planet
from ai_models.basic_ai import BasicAI
from utils.animation import Animation
from training.ai_trainer import train_ai_model, get_latest_model

FUEL_DENSITY = 0.05
TRAINING = True
RESET_MODEL = False

logging.basicConfig(level=logging.WARNING, force=True)
    
def main():
    # Argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Lander simulation")
    parser.add_argument('--display', action='store_true', help="Enable display for animation")
    parser.add_argument('--training', action='store_true', help="Launch ai-model training")
    
    args = parser.parse_args()

    if args.training or TRAINING:
        train_ai_model(num_episodes=10000, save_interval=100, reset_model=RESET_MODEL)
        return 0

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

    max_thrust = random.uniform(500, 5000)
    max_fuel = random.uniform(500, 5000)
    drag_coeff = random.uniform(0.2, 0.8) 
    surface_area = random.uniform(1.0, 10.0)    
    
    mass = max_fuel*FUEL_DENSITY + max_thrust/200
    
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
    ai_model = BasicAI(lander, planet)
    save_dir="ai_models/models_saved"
    latest_model = get_latest_model(save_dir)
    if latest_model :
        ai_model.ai_model.load(latest_model)

    # Create the Animation object without display
    animation = Animation(lander, ai_model, planet, start_position,
                          total_time=100.0, display=args.display)

    # Run the simulation (no display)
    animation.run()
    
    return 0

if __name__ == "__main__" :
    main()
