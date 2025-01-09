def reward_function(params):

    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']

    reward = 1e-3

    # センターラインから離れた距離を3つの段階で評価する
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # センターラインから離れた距離により上記で計算した3段階に分けて報酬を設定
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # クラッシュ時もしくはオフトラックに近づいている状態

    # Always return a float value
    return float(reward)
