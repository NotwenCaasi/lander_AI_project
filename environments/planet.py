# environments/planet.py

import numpy as np
import matplotlib.pyplot as plt

class Planet:
    def __init__(self, radius, atmosphere_thickness, air_ground_density, gravity_constant):
        self.radius = radius
        self.atmosphere_thickness = atmosphere_thickness
        self.air_ground_density = air_ground_density
        self.gravity_constant = gravity_constant
        
        self.ground_length = radius * 2 * np.pi  # Circumference of the planet

        # Generate the terrain with a flat landing area
        self.terrain, self.landing_zone = self.generate_terrain()
        

    def atmosphere_density(self, altitude):
        """
        Returns the relative air density at a given altitude.
        """
        thickness = self.atmosphere_thickness
        if altitude >= thickness:
            return 0
        elif altitude <= 0:
            return self.air_ground_density
        else:
            air_density = (1 - (altitude / thickness)) * self.air_ground_density
            return air_density

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
        
        y0 = np.average(y)

        # Create a flat landing area
        flat_start = int((num_points - flat_length / total_length * num_points) // 2)
        flat_end = flat_start + int(flat_length / total_length * num_points)
        y[flat_start:flat_end] = 0  # Flat landing zone

        landing_zone = [[flat_start, y0], [flat_end, y0]]

        return list(zip(x, y)), landing_zone

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
planet = Planet(radius=6000, atmosphere_thickness=1000, air_ground_density=1.0, gravity_constant=9.8)
planet.display_terrain()
