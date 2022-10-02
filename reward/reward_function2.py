import math

'''
Input: dict type
Document: https://docs.aws.amazon.com/ja_jp/deepracer/latest/developerguide/deepracer-reward-function-input.html?icmpid=docs_deepracer_console
'''

def reward_function(params):
    '''
    この関数の中でやっていること
    1. 経路の角度と進行方向の差分を比較
    2. ジグザグ走行抑制
    3. 300ステップごとに追加の報酬を設定
    '''
    reward = 1e-3

    # 得られたparamsからパラメータを読み込む
    all_wheels_on_track = params["all_wheels_on_track"]      # flag to indicate if the agent is on the track
    x = params["x"]                                           # float, agent's x-coordinate in meters
    y = params["y"]                                           # float, agent's y-coordinate in meters
    closest_waypoints = params["closest_waypoints"]           # [int, int], indices of the two nearest waypoints.
    distance_from_center = params["distance_from_center"]     # float, distance in meters from the track center
    is_left_of_center = params["is_left_of_center"]           # Boolean, Flag to indicate if the agent is on the left side to the track center or not.
    is_offtrack = params["is_offtrack"]                       # Boolean flag to indicate whether the agent has gone off track.
    is_reserved = params["is_reversed"]                       # Boolean, flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    heading = params["heading"]                               # float, agent's yaw in degrees
    progress = params["progress"]                             # float, percentage of track completed
    speed = params["speed"]                                   # float, agent's speed in meters per second (m/s)
    steering_angle = params["steering_angle"]                 # float, agent's steering angle in degrees
    steps = params["steps"]                                   # int, number steps completed
    track_length = params["track_length"]                     # float, track length in meters.
    track_width = params["track_width"]                       # float, width of the track
    waypoints = params["waypoints"]                           # [(float, float), list of (x,y) as milestones along the track center


    #---------進行方向の角度の比較--------------------

    # 前回のway pointと次のway pointを設定する
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

    # 自分の角度とコースの角度の差分算出
    direction_diff = track_direction - heading

    # 差分を＋/-180度以内に変換する
    direction_diff = (direction_diff + 180) % 360 - 180

    # 速度&ハンドル
    # より早いスピードであれば高い報酬を設定
    reward = reward + speed/6

    # もし角度の差分が大きければ角度によってペナルティを与える

    # 角度が12以下でかつハンドルの角度が0の場合(ハンドルを切っていない場合)
    if direction_diff <= 12 and steering_angle == 0:
        reward += speed/6
    # 角度が大きい場合には、速度に応じたペナルティを設定する
    elif abs(direction_diff) > 12:
        reward -= speed/6

    # ---理想的なラインに従う---


    # ---ジグザグ運転防止---
    '''
    ジグザグ運転を抑えるためのステアリングへのペナルティ
    '''
    abs_steering = abs(steering_angle)
    ABS_STEERING_THRESHOLD = 15
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # ---ステップごとに報酬を追加---
    # 100ステップごとに、予測より進捗が高かったら追加報酬を設定
    expected_steps = 300
    if (steps % 100) == 0 and progress > (steps / expected_steps) * 100:
        reward += 5.0

    return float(reward)
