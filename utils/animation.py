# utils/animation.py

import logging
from environments.physics import update_lander_state
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

logging.basicConfig(level=logging.INFO)

class Animation:
    def __init__(self, lander, ai_model, planet, start_position, total_time=100, dt=0.1, display=True):
        self.lander = lander
        self.ai_model = ai_model
        self.planet = planet
        self.start_position = start_position
        self.total_time = total_time
        self.dt = dt
        self.display = display  # Controls whether display is enabled or not
        self.ani = None  # Placeholder for animation object if used
        self.fig = None
        self.ax = None

    def update(self, frame):
        # AI controls the lander
        thrust, angle = self.ai_model.control()
        logging.info(f"Frame {frame}: Thrust = {thrust}, Angle = {angle}")
        
        # Update the lander physics
        update_lander_state(self.lander, self.planet, self.dt)
        logging.info(f"Frame {frame}: Position: {self.lander.position}, Velocity: {self.lander.velocity}, Fuel: {self.lander.fuel}")

        if self.display:
            # Update the marker in the display
            self.lander_marker.set_data([self.lander.position[0]], [self.lander.position[1]])
            return self.lander_marker,  # Ensure the marker is returned as a tuple

    def setup_display(self):
        """Setup the display for animation."""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        x, y = zip(*self.planet.terrain)
        self.ax.plot(x, y, label="Terrain")
        self.ax.set_ylim(-200, self.planet.atmosphere_thickness)
        self.ax.set_xlim(0, self.planet.ground_length)

        # Initialize lander plot
        self.lander_marker, = self.ax.plot([], [], 'ro', label="Lander")
        plt.legend()
        plt.title("Lander Descent Animation")

    def run(self):
        """Run the simulation."""
        # Reset the lander to its initial position
        self.lander.reset(self.start_position)
        logging.info(f"Lander reset to start position: {self.start_position}")

        if self.display:
            # Setup the display for animation
            self.setup_display()

            # Create and run the animation
            logging.info(f"Running animation for {self.total_time} seconds.")
            self.ani = FuncAnimation(
                self.fig, self.update, frames=int(self.total_time / self.dt), 
                blit=False, interval=100, repeat=False)
            plt.show()  # Only call plt.show() here for animation display
        else:
            # No display, just run the physics update
            for frame in range(int(self.total_time / self.dt)):
                self.update(frame)
