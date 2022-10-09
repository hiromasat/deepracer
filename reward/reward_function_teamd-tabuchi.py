import math


def reward_function(params):

    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    closest_waypoints = params["closest_waypoints"]
    heading = params["heading"]
    speed = params["speed"]
    steering_angle = params["steering_angle"]
    waypoints = params["waypoints"]

    # Give a very low reward by default
    reward = 1e-3

    prev_point = waypoints[closest_waypoints[0]]
    next_point = waypoints[closest_waypoints[1]]

    # コーストラックの角度を計算する
    # 2つの近接するway pointよりトラックの向きを計算する(戻り値はradian、pi〜-pi)
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # 角度に変換する
    track_direction = math.degrees(track_direction)

    if track_direction < 0:
        track_direction += 360
        reward = 1e-3

    # トラックから外れた場合に最小の報酬を設定する
    if not all_wheels_on_track:
        reward = 1e-3
    else:
        # トラックに乗っていてトラックの半分幅と距離が0.05 であれば高い報酬を設定
        if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
            reward = 1.0

        # より早いスピードであれば高い報酬を設定
        reward = reward + speed / 6

        # コースのトラックの向きと、エージェントの進む角度の差分
        direction_diff = track_direction - heading

        # 差分を＋/-180度以内に変換する
        direction_diff = (direction_diff + 180) % 360 - 180

        # もし角度の差分が大きければ角度によってペナルティを与える
        reward = reward + 1 - direction_diff / 90

        # 角度が12以下でかつハンドルの角度が0の場合(ハンドルを切っていない場合)
        if direction_diff <= 12 and steering_angle == 0:
            reward += 1
        # 角度が大きい場合には、ハンドルを切っている角度に応じたペナルティを設定する
        elif abs(direction_diff) > 12:
            reward = reward + 1 - abs(direction_diff - steering_angle) / 30
        # ハンドルを切った角度に応じてペナルティを設定する
        reward = reward + 1 - abs(steering_angle) / 24

    return float(reward)
