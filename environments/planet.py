# environments/planet.py

import numpy as np
import matplotlib.pyplot as plt

class Planet:
    def __init__(self, radius, atmosphere_thickness, gravity_constant):
        self.radius = radius
        self.atmosphere_thickness = atmosphere_thickness
        self.gravity_constant = gravity_constant
        self.ground_length = radius * 2 * np.pi  # Circumference of the planet

        # Generate the terrain with a flat landing area
        self.terrain = self.generate_terrain()

    def atmosphere_density(self, altitude):
        """
        Returns the relative air density at a given altitude.
        """
        thickness = self.atmosphere_thickness
        if altitude >= thickness:
            return 0
        elif altitude <= 0:
            return 1
        else:
            return 1 - (altitude / thickness)

    def generate_terrain(self, flat_length=1000):
        """
        Generates periodic terrain as a list of points (x, y) with a flat landing area.
        - flat_length: Length of the flat landing area.
        """
        total_length = self.ground_length
        num_points = 100  # Number of points to define the terrain

        # Define the x-coordinates
        x = np.linspace(0, total_length, num_points)

        # Generate terrain with random heights
        y = np.random.uniform(-200, 200, size=num_points)

        # Make sure the terrain is periodic by setting y[0] = y[-1]
        y[-1] = y[0]

        # Create a flat landing area
        flat_start = int((num_points - flat_length / total_length * num_points) // 2)
        flat_end = flat_start + int(flat_length / total_length * num_points)
        y[flat_start:flat_end] = 0  # Flat landing zone

        return list(zip(x, y))

    def display_terrain(self):
        """
        Display the terrain using matplotlib.
        """
        x, y = zip(*self.terrain)
        plt.plot(x, y)
        plt.title("Periodic Terrain of the Planet with Flat Landing Area")
        plt.xlabel("Ground length (m)")
        plt.ylabel("Height (m)")
        plt.show()

# Example usage
planet = Planet(radius=6000, atmosphere_thickness=1000, gravity_constant=9.8)
planet.display_terrain()
