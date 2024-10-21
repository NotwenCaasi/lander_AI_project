# utils/animation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from environments.physics import update_lander_state
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

class Animation:
    def __init__(self, lander, ai_model, planet, start_position, total_time=100, dt=0.1, display=True):
        self.lander = lander
        self.ai_model = ai_model
        self.planet = planet
        self.start_position = start_position
        self.total_time = total_time
        self.dt = dt
        self.display = display
        self.fig, self.ax = None, None
        self.ani = None  # Keep the animation object as a persistent instance variable

    def update(self, frame):
         logging.info(f"Running frame {frame}...")  # Added to track frame execution
         
         # AI controls the lander
         thrust, angle = self.ai_model.control(self.lander.get_state())
         logging.info(f"Frame {frame}: Thrust = {thrust}, Angle = {angle}")
         
         # Update the lander physics
         update_lander_state(self.lander, self.planet, self.dt)
         logging.info(f"Frame {frame}: Position: {self.lander.position}, Velocity: {self.lander.velocity}, Fuel: {self.lander.fuel}")
         
         if self.display:
             # Update the display (lander position, fuel text, etc.)
             self.lander_marker.set_data([self.lander.position[0]], [self.lander.position[1]])  # Pass as lists
             self.fuel_text.set_text(f"Fuel: {self.lander.fuel:.1f}%\nSpeed: {self.lander.velocity[1]:.2f} m/s")
             return self.lander_marker, self.fuel_text  # Always return updated artists

    def setup_display(self):
        """Set up the display for animation (only used if self.display is True)."""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        x, y = zip(*self.planet.terrain)
        self.ax.plot(x, y, label="Terrain")
        self.ax.set_ylim(-200, self.planet.atmosphere_thickness)  # Limit y-axis to atmosphere thickness
        self.ax.set_xlim(0, self.planet.ground_length)

        # Initialize lander plot
        self.lander_marker, = self.ax.plot([], [], 'ro', label="Lander")
        self.fuel_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)

        plt.legend()
        plt.title("Lander Descent Animation")

    def run(self):
        """Run the simulation with or without display."""
        # Reset the lander to its initial position
        self.lander.reset(self.start_position)
        logging.info(f"Lander reset to start position: {self.start_position}")

        if self.display:
            # Set up the display for animation
            self.setup_display()

            # Run the animation and assign to self.ani to prevent garbage collection
            logging.info(f"Running animation for {self.total_time} seconds.")
            self.ani = FuncAnimation(self.fig, self.update, frames=int(self.total_time / self.dt), blit=False, interval=100)
            plt.show()
        else:
            # No display, just update physics
            for frame in range(int(self.total_time / self.dt)):
                self.update(frame)
