# -*- coding: utf-8 -*-

def collect_training_data(lander, planet, frame_data):
    # Extract and store relevant data
    frame_data.append({
        'position': lander.position,
        'velocity': lander.velocity,
        'fuel': lander.fuel,
        'thrust': lander.thrust,
        'angle': lander.angle,
        'gravity': planet.gravity_constant,
        'air_density': planet.get_air_density(lander.position[1])
    })
