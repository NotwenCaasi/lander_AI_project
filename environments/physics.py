# -*- coding: utf-8 -*-
# Contains planet environments and simulations
# Physics calculations (gravity, drag, etc.)
# environments/physics.py

import numpy as np

def compute_drag(velocity, drag_coeff, air_density, surface_area):
    """Compute the drag force based on velocity and atmosphere properties."""
    drag_force = -0.5 * air_density * drag_coeff * surface_area * np.linalg.norm(velocity) * velocity
    return drag_force

def update_lander_state(lander, planet, dt):
    """Update the lander's position based on physics (gravity, drag, thrust)."""
    if lander.fuel <= 0 or lander.is_landed:
        return

    # Compute the atmosphere density at the current altitude
    altitude = lander.position[1]
    air_density = planet.atmosphere_density(altitude)

    # Gravity force
    gravity_force = np.array([0, -lander.mass * planet.gravity_constant])

    # Drag force
    drag_force = compute_drag(lander.velocity, lander.drag_coeff, air_density, lander.surface_area)

    # Thrust force (assume thrust is applied directly opposite of gravity)
    thrust_force = np.array(
        [lander.thrust*lander.max_thrust * np.sin(np.radians(lander.angle)),
         lander.thrust*lander.max_thrust * np.cos(np.radians(lander.angle))])

    # Total force on the lander
    total_force = gravity_force + drag_force + thrust_force

    # Update velocity and position
    acceleration = total_force / lander.mass
    lander.velocity += acceleration * dt
    lander.position += lander.velocity * dt

    # Check for collision with the ground
    if lander.position[1] <= 0:  # Ground collision
        lander.position[1] = 0
        lander.velocity[1] = 0
        lander.is_landed = True

    # Update fuel usage (assume constant consumption per unit of thrust)
    lander.fuel -= lander.thrust*lander.max_thrust * dt
    
    return 0
