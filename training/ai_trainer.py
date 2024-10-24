# -*- coding: utf-8 -*-

# training/ai_trainer.py

import random
import torch
import re
import csv
import os

from lander.lander import Lander
from environments.planet import Planet
from ai_models.basic_ai import BasicAI
from utils.animation import Animation

FUEL_DENSITY = 0.1
MAX_THRUST = 2000
SURFACE_AREA = 4.0
DRAG_COEFF = 0.5
MAX_FUEL = 100
    
MASS = MAX_FUEL*FUEL_DENSITY+MAX_THRUST/200


def get_latest_model(save_dir):
    """Find the latest saved model in the specified directory."""
    files = [f for f in os.listdir(save_dir) if re.match(r'ai_model_episode_\d+\.pth', f)]
    if not files:
        return None
    # Sort by episode number and return the latest
    latest_model = max(files, key=lambda x: int(re.search(r'\d+', x).group()))
    return os.path.join(save_dir, latest_model)

def save_training_loss(epoch, reward, loss_file='training_loss.csv'):
    """Append the total reward for the current epoch to the loss file."""
    with open(loss_file, 'a') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow([epoch, reward])
        
def train_ai_model(num_episodes=10000, reset_model=False, save_interval=100, save_dir="ai_models/models_saved", loss_file='training_loss.csv'):
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)
   
    # Initialize the AI model (this should be done ONCE at the start, not every episode)
    planet = Planet()
    lander = Lander(max_thrust=1500, max_fuel=500, drag_coeff=0.5, mass=1000, surface_area=4.0)
    ai_model = BasicAI(lander, planet)
    ai_model.prepare_for_landing()

    start_episode = 0
    
    # Check if a model already exists and load it
    if not reset_model:
        latest_model = get_latest_model(save_dir)
    
        if latest_model:
            # Extract the episode number from the file name
            start_episode = int(re.search(r'\d+', latest_model).group())
            print(f"Resuming from episode {start_episode + 1}")
            ai_model.ai_model.load(latest_model)
            print(f"Loading model from {latest_model}")
    
    for episode in range(start_episode, num_episodes):
        # Create a random planet
        planet = Planet()
        # Set random start position
        start_x = random.uniform(0, planet.ground_length)
        start_y = planet.atmosphere_thickness
        start_v = random.uniform(-10, 0)
        start_t = 0
        start_a = random.uniform(-90, 90)
        start_position = (start_x, start_y, start_v, start_t, start_a)  # x, y, v, t, a

        # Initialize the lander
        max_thrust = random.uniform(500, 5000)
        max_fuel = random.uniform(500, 5000)
        drag_coeff = random.uniform(0.2, 0.8) 
        surface_area = random.uniform(1.0, 10.0)    
        
        mass = max_fuel*FUEL_DENSITY + max_thrust/200
        
        lander = Lander(max_thrust=max_thrust, max_fuel=max_fuel, drag_coeff=drag_coeff, mass=mass, surface_area=surface_area)
        lander.reset(start_position)
        
        ai_model.lander = lander
        ai_model.planet = planet
        ai_model.prepare_for_landing()

        # Initialize the animation (set display=False for training)
        animation = Animation(lander, ai_model, planet, start_position, display=False)

        # Run the simulation
        animation.run()

        # At the end of the episode, print the results
        total_reward = sum([experience[2] for experience in ai_model.ai_model.memory])  # Sum of rewards
        print(f"Episode {episode+1}/{num_episodes}, Total Reward: {total_reward}, Epsilon: {ai_model.ai_model.epsilon}")

        # Save the total_reward in training_loss.csv
        save_training_loss(episode + 1, total_reward, loss_file)
        
        # Optionally save the model every few episodes
        if (episode + 1) % save_interval == 0:
            ai_model.ai_model.save(f"{save_dir}/ai_model_episode_{episode+1}.pth")
        
