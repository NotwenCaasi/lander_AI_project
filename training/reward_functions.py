# -*- coding: utf-8 -*-

def compute_reward(lander):
    if lander.has_landed_smoothly():
        return 100  # High reward for a successful landing
    elif lander.crashed():
        return -100  # Penalty for crashing
    else:
        return -1  # Small penalty for each step (to encourage quicker landings)
