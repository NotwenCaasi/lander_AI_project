# -*- coding: utf-8 -*-

# utils/live_plot.py

import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import numpy as np

def load_training_loss(filepath='training_loss.csv'):
    """Load the training loss data from the CSV file."""
    if os.path.exists(filepath):
        # Read the file with space as the delimiter
        data = pd.read_csv(filepath, sep=' ', header=None, names=['Epoch', 'Total Reward'])
        return data
    else:
        return pd.DataFrame(columns=['Epoch', 'Total Reward'])

def reset_curve(epoch_data):
    """Helper function to reset curve index based on restart of epochs."""
    curves = []
    curve = []
    last_epoch = epoch_data[0][0]  # Initialize the first epoch (extract the epoch value)
    
    for epoch, reward in epoch_data:
        if epoch < last_epoch:  # Compare only the epoch value
            curves.append(curve)
            curve = []
        curve.append(reward)
        last_epoch = epoch
    curves.append(curve)  # Append the last curve
    return curves

def live_plot_training_loss(filepath='training_loss.csv', refresh_interval=60):
    """Plot the training loss live with periodic refreshes and a logarithmic scale."""
    plt.ion()  # Turn on interactive mode for live plotting
    fig, ax = plt.subplots()
    
    ax.set_yscale('log')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Total Reward (Positive, Log scale)')
    ax.set_title('Live Training Reward Plot (Logarithmic Scale)')
    
    while True:
        # Load the latest data from the CSV
        data = load_training_loss(filepath)

        if not data.empty:
            # Extract epoch and reward data
            epoch_data = list(zip(data['Epoch'], data['Total Reward'].abs()))  # Ensure positive values for the log scale
            
            # Split data into separate curves when epoch number restarts
            curves = reset_curve(epoch_data)

            ax.clear()
            ax.set_yscale('log')
            ax.set_xlabel('Epoch')
            ax.set_ylabel('Total Reward (Positive, Log scale)')
            ax.set_title('Live Training Reward Plot (Logarithmic Scale)')

            # Plot each curve
            num_curves = len(curves)
            for i, curve in enumerate(curves[:-1]):
                intensity = (num_curves-1-i) / (num_curves - 1)  # Intensity based on curve age
                grey_color = (intensity, intensity, intensity)  # Create a grey color
                ax.plot(np.arange(len(curve)), curve, linestyle=':', color=grey_color)

            # Plot the current curve in red continuous line
            current_curve = curves[-1]
            ax.plot(np.arange(len(current_curve)), current_curve, color='red', linestyle='-', label='Current Curve')

            ax.legend()
            plt.draw()  # Update the plot
            plt.pause(0.1)  # Pause for a brief moment to allow the plot to update

        # Wait before refreshing again
        time.sleep(refresh_interval)

if __name__ == "__main__":
    # Start the live plot with a refresh interval of 60 seconds
    live_plot_training_loss(refresh_interval=60)
