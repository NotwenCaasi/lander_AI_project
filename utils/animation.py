# utils/animation.py

import logging
import matplotlib.pyplot as plt

from environments.physics import update_lander_state
from matplotlib.animation import FuncAnimation
from training.reward_functions import compute_reward


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
        
        # Initialize previous distances to target at the start of the episode
        self.prev_dx = min(abs(self.lander.position[0] - self.ai_model.landing_x_center),
                        abs(self.lander.position[0]+self.planet.ground_length - self.ai_model.landing_x_center))   
        self.prev_dy = abs(self.lander.position[1] - self.ai_model.landing_y_center)
        # Initialize previous fuel level
        self.prev_fuel = 100
        
    def update(self, frame):
        # Get the current state
        state = self.ai_model.get_state_vector()
        # AI controls the lander
        thrust, angle_change, thrust_idx, angle_idx = self.ai_model.control()
        logging.info(f"Frame {frame}: Thrust = {thrust}, Angle Change = {angle_change}")

        # Update the lander physics
        update_lander_state(self.lander, self.planet, self.dt)
        logging.info(f"Frame {frame}: Position: {self.lander.position}, Velocity: {self.lander.velocity}, Fuel: {self.lander.fuel}")

        # Get the next state
        next_state = self.ai_model.get_state_vector()
        
        # Compute reward
        r1, r2, r3, r4, r5, r6, r7, r8 = compute_reward( 
             self.lander, self.planet.landing_zone, self.prev_dx, self.prev_dy, self.prev_fuel)
        reward = r1
        distance_reward = r2
        v_speed_penalty = r3
        h_speed_penalty = r4
        fuel_penalty = r5
        self.prev_dx = r6
        self.prev_dy = r7
        self.prev_fuel = r8

        done = self.lander.crashed or self.lander.is_landed
        
        # Log individual reward components
        logging.info(f"Frame {frame}: Total Reward = {reward}, "
                     f"Distance Reward = {distance_reward}, "
                     f"Vertical Speed Penalty = {v_speed_penalty}, "
                     f"Horizontal Speed Penalty = {h_speed_penalty}, "
                     f"Fuel Penalty = {fuel_penalty}")
        

        # Remember the experience
        self.ai_model.ai_model.remember(state, (thrust_idx, angle_idx), reward, next_state, done)
        # Train the AI model
        self.ai_model.ai_model.replay()

        if self.display:
            if self.lander.crashed:
                logging.info(f"Lander crashed at frame {frame}. Stopping simulation.")
                self.lander_marker.set_marker('x')
                self.ani.event_source.stop()
                return
            # Update the marker in the display
            self.lander_marker.set_data([self.lander.position[0]], [self.lander.position[1]])
            return self.lander_marker,

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
