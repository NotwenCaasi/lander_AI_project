# -*- coding: utf-8 -*-

# training/reward_functions.py

def compute_reward(lander, landing_zone, prev_dx, prev_dy, prev_fuel):
    # Distance to landing zone at current time step
    landing_x_center = (landing_zone[0][0] + landing_zone[1][0]) / 2
    landing_y_center = landing_zone[0][1]
    current_dx = abs(lander.position[0] - landing_x_center)
    current_dy = lander.position[1] - landing_y_center  # Should be close to 0 for landing

    # Change in distance from the previous time step
    delta_dx = prev_dx - current_dx
    delta_dy = prev_dy - current_dy

    # Vertical and horizontal speed
    vertical_speed = abs(lander.velocity[1])
    horizontal_speed = abs(lander.velocity[0])

    # Fuel used since last step
    fuel_used_step = (prev_fuel - lander.fuel)*lander.max_fuel

    # Distance reward: Encourage reduction in distance to the target
    distance_reward = delta_dx * 1.0 + delta_dy * 1.0
            
    # Speed penalties
    vertical_speed_penalty = -vertical_speed * 0.05  # Penalize high vertical speed
    horizontal_speed_penalty = -horizontal_speed * 0.02  # Penalize horizontal speed

    # Fuel penalty
    fuel_penalty = -fuel_used_step*0.01  # Penalize fuel usage

    # Total reward sum
    total_reward = distance_reward + vertical_speed_penalty + horizontal_speed_penalty + fuel_penalty

    # Landing success
    if lander.is_landed:
        landing_bonus = 1000
        total_reward += landing_bonus
        total_reward += -vertical_speed * 10  # Strong penalty for landing with high vertical speed
        total_reward += - (100 - lander.fuel)*lander.max_fuel* 0.5  # Reward for fuel-efficient landing

    elif lander.crashed:
        crash_penalty = -1000
        total_reward = crash_penalty
    else:
        # Small time penalty to encourage faster landings
        total_reward += -1
    
    if current_dx < 10 and current_dy < 10:  # If very close to landing zone
        total_reward += 50  # Small bonus for good proximity

    return total_reward, distance_reward, vertical_speed_penalty, horizontal_speed_penalty, fuel_penalty, current_dx, current_dy, lander.fuel
