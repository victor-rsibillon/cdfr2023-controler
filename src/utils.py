def default_config(environment: dict) -> None:
    environment['coords_x'] = 0
    environment['coords_y'] = 0
    environment['coords_r'] = 0
    environment['colliding_front'] = False
    environment['colliding_back'] = False
    environment['colliding_distance'] = float('inf')
    environment['grace_full_shutdown'] = False
    environment['moving_state'] = 1  # -1 if going backward, 0 if static, 1 if going forward