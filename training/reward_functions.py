# -*- coding: utf-8 -*-


def compute_reward(lander, landing_zone):
    # Reward based on how close the lander is to the landing zone
    distance_to_target = abs(lander.position[0] - landing_zone[0]) + abs(lander.position[1] - landing_zone[1])
    vertical_speed_penalty = abs(lander.velocity[1])
    horizontal_speed_penalty = abs(lander.velocity[0])
    fuel_penalty = lander.fuel

    if distance_to_target < 50 and vertical_speed_penalty < 5:
        return 1000  # High reward for successful landing
    elif lander.position[1] <= 0 and vertical_speed_penalty >= 5:
        return -100  # Penalty for crashing
    else:
        return -distance_to_target - fuel_penalty  # Penalty for bad landing or fuel consumption
