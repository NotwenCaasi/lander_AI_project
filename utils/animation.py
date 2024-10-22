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
            if self.lander.crashed:
                logging.info(f"Lander crashed at frame {frame}. Stopping simulation.")
                self.lander_marker.set_marker('x')
                self.ani.event_source.stop()
                return  # Stop updating if lander has crashed
            # Update the marker in the display
            self.lander_marker.set_data([self.lander.position[0]], [self.lander.position[1]])
            return self.lander_marker,  # Ensure the marker is returned as a tuple

    def setup_display(self):
        """Setup the display for animation."""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Set the background color to black
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')

        # Plot the terrain in white
        x, y = zip(*self.planet.terrain)
        self.ax.plot(x, y, color="white", label="Terrain")

        # Set limits for the display
        self.ax.set_ylim(-200, self.planet.atmosphere_thickness)
        self.ax.set_xlim(0, self.planet.ground_length)

        # Remove axis ticks and labels
        self.ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # Initialize lander plot with a red marker
        self.lander_marker, = self.ax.plot([], [], 'ro', label="Lander")

        # Set the title in white and adjust the legend color
        plt.legend(facecolor='black', edgecolor='white')
        plt.title("Lander Descent Animation", color="white")

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
                if self.lander.crashed:
                    logging.info(f"Simulation stopped at frame {frame} due to crash.")
                    break
