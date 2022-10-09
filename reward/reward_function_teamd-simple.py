def reward_function(params):
    '''
    トラックの2つのボーダーの間にいるときに報酬を与える
    '''

    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']

    reward = 1e-3

    # トラックから外れておらず、エージェントがトラックに乗っている場合に高い報酬を設定
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Always return a float value
    return float(reward)
