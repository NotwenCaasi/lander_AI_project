# -*- coding: utf-8 -*-
# Contains planet environments and simulations
# Physics calculations (gravity, drag, etc.)
# environments/physics.py

import numpy as np
import logging
import bisect

MAX_HORIZONTAL_LANDING_SPEED = 5
MAX_VERTICAL_LANDING_SPEED = 5

def compute_drag(velocity, drag_coeff, air_density, surface_area):
    """Compute the drag force based on velocity and atmosphere properties."""
    drag_force = -0.5 * air_density * drag_coeff * surface_area * np.linalg.norm(velocity) * velocity
    return drag_force

def update_lander_state(lander, planet, dt):
    """Update the lander's position based on physics (gravity, drag, thrust)."""
    if lander.is_landed:
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
    if lander.position[0]>planet.ground_length :
        lander.position[0] -= planet.ground_length
    elif lander.position[0] < 0 :
        lander.position[0] += planet.ground_length
    else:
        pass
    
    # Check for terrain collision (lander's y position should be above the terrain)
    landed_or_crashed = detect_terrain_collision(lander, planet)
    if landed_or_crashed == 'flying':
        pass
    elif landed_or_crashed == 'crashed':
        lander.crashed = True
        logging.info("Lander has crashed !")
    elif landed_or_crashed == 'landed':
        lander.is_landed = True
        logging.info("Lander has landed !! !oo! !!")
        
    # Update the lander's position only if it has not crashed
    if not lander.crashed:
        lander.position[0] += lander.velocity[0] * dt  # Update x position
        lander.position[1] += lander.velocity[1] * dt  # Update y position

    # Update fuel usage (assume constant consumption per unit of thrust)
    df = lander.thrust*lander.max_thrust * dt/lander.max_fuel
    logging.info(f"fuel variation = {df}")
    lander.fuel -= df
    lander.fuel = max(0, lander.fuel)
    
    
    
    return 0

def detect_terrain_collision(lander, planet):
    """Check if the lander's position is below the terrain."""

    # Find the terrain height at the lander's current x position
    terrain_height = get_terrain_height_at_x(lander, planet.terrain)
    
    # If the lander's y position is below the terrain height, return True (crash detected)
    if lander.position[1] <= terrain_height:
        if lander.position[0] >= planet.landing_zone[0][0]:
            if lander.position[0] <= planet.landing_zone[1][0]:
                if lander.angle == 0:
                    if abs(lander.velocity[0]) < MAX_HORIZONTAL_LANDING_SPEED:
                        if lander.velocity[1] > -MAX_VERTICAL_LANDING_SPEED:
                            return 'landed'
        return 'crashed'
    return 'flying'

def get_terrain_height_at_x(lander, terrain):
    """Find the terrain height at the given x position using the lander's cached terrain index."""
    x = lander.position[0]

    # Unzip the terrain into two separate lists for x and y coordinates
    terrain_x, terrain_y = zip(*terrain)

    # Check if the cached terrain segment is still valid
    if terrain_x[lander.last_terrain_idx] <= x <= terrain_x[lander.last_terrain_idx + 1]:
        # Use the cached segment to compute the height
        x1, y1 = terrain[lander.last_terrain_idx]
        x2, y2 = terrain[lander.last_terrain_idx + 1]
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    # Perform binary search to find the correct segment if outside cached segment
    lander.last_terrain_idx = bisect.bisect_left(terrain_x, x) - 1
    lander.last_terrain_idx = max(0, min(lander.last_terrain_idx, len(terrain_x) - 2))

    # Now that we found the correct segment, calculate the terrain height
    x1, y1 = terrain[lander.last_terrain_idx]
    x2, y2 = terrain[lander.last_terrain_idx + 1]
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
