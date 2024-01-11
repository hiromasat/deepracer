# -*- coding: utf-8 -*-
#
import math
def reward_function(params):

    # デフォルトの報酬値
    reward = 1.0

    # コース内に収まっている状態を判定
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    steering_angle = params['steering_angle']
    waypoints = params['waypoints']
    near_waypoints = params['closest_waypoints']
    heading = params['heading']

    # コースを外れたらペナルティ(小さな報酬関数)
    if not all_wheels_on_track:
        reward = 1e-3
        return reward

    # コースと動態の角度の差分を算出

    next_point = waypoints[near_waypoints[1]]
    prev_point = waypoints[near_waypoints[0]]

    # 前のwaypointから次のwaypointに向かう角度(radian)を計算する
    # math.atan2(y, x) -> 角度[rad]
    # math.degrees(param) -> 角度[deg]
    track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))

    # コースの向きと、動態の角度の差分
    delta  = track_direction - heading

    # センターラインからの離れ度合い
    marker_1 = 0.2 * track_width
    marker_2 = 0.5 * track_width
    marker_3 = 0.75 * track_width

    # ステアリング操作を報酬に反映させる
    # is_left_of_center：トラック中心から左右のどちらにいるか？
    # steering_angle；ハンドルの角度（+:ledt、-:right)

    # センターラインに近いほど多めの報酬を与える
    if distance_from_center <= marker_1:
        reward = 1.0


    # センターラインから
    elif distance_from_center <= marker_2:
        if is_left_of_center:
            if delta >= 0 and delta < 30:
                reward = 0.5
            else:
                reward = 1e-3
        else:
            if delta < 0 and delta > - 30:
                reward = 0.5
            else:
                reward = 1e-03

    # センターラインから
    elif distance_from_center <= marker_3:
        if is_left_of_center:
            if delta >= 20 and delta < 50:
                reward = 0.5
            else:
                reward = 1e-3
        else:
            if delta < -20 and delta > -50:
                reward = 0.5
            else:
                reward = 1e-03
    else:
        reward = 1e-3

    return float(reward)