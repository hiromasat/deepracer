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
    delta_angle  = track_direction - heading

    # センターラインからの離れ度合い
    marker_1 = 0.2 * track_width
    marker_2 = 0.5 * track_width
    marker_3 = 0.75 * track_width

    # ステアリング操作を報酬に反映させる
    # is_left_of_center：トラック中心から左右のどちらにいるか？
    # steering_angle；ハンドルの角度（+:ledt、-:right)

    # センターラインから離れ具合が25%以下(センターラインに近い場所を走っている)
    # センターラインに近いほど多めの報酬を与える
    if distance_from_center <= marker_1:
        reward = 1.0


    # センターラインから離れ具合が50%以下
    elif distance_from_center <= marker_2:
        if is_left_of_center:  # 左にいる場合
            # センターラインをどのくらい向いているか。（センターラインの方向を向いていたら報酬を与える）
            if delta_angle >= 0 and delta_angle < 30:
                reward = 0.5
            else:
                reward = 1e-3
        else:  # 右にいる場合
            # センターラインをどのくらい向いているか。（センターラインの方向を向いていたら報酬を与える）
            if delta_angle < 0 and delta_angle > - 30:
                reward = 0.5
            else:
                reward = 1e-03

    # センターラインから離れ具合が75%以下
    elif distance_from_center <= marker_3:
        if is_left_of_center:
            # センターラインをどのくらい向いているか。（センターラインの方向を向いていたら報酬を与える）
            if delta_angle >= 20 and delta_angle < 50:
                reward = 0.5
            else:
                reward = 1e-3
        else:
            # センターラインをどのくらい向いているか。（センターラインの方向を向いていたら報酬を与える）
            if delta_angle < -20 and delta_angle > -50:
                reward = 0.5
            else:
                reward = 1e-03
    else:
        reward = 1e-3

    return float(reward)