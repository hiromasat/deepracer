import math

'''
Input: dict type
Document: https://docs.aws.amazon.com/ja_jp/deepracer/latest/developerguide/deepracer-reward-function-input.html?icmpid=docs_deepracer_console
'''

class Reward:
    def __init__(self):
        self.first_racingpoint_index = None
        self.previous_params = None

    def reward_function(self, params):
        '''
        この関数の中でやっていること
        1. self.previous_paramsには前回よばれた時のparamsが保存されている(初回はNone)
        2. 報酬を計算
        3. 今回のparamsをprevious_paramsにセットして保持する
        '''

        # 得られたparamsからパラメータを読み込む

        all_wheels_on_track = params["all_wheels_on_track"],      # flag to indicate if the agent is on the track
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

        # previopus paramsからパラメータを読み込む
        all_wheels_on_track_p = previous_params["all_wheels_on_track"],      # flag to indicate if the agent is on the track
        x_p = previous_params["x"]                                           # float, agent's x-coordinate in meters
        y_p = previous_params["y"]                                           # float, agent's y-coordinate in meters
        closest_waypoints_p = previous_params["closest_waypoints"]           # [int, int], indices of the two nearest waypoints.
        distance_from_center_p = previous_params["distance_from_center"]     # float, distance in meters from the track center
        is_left_of_center_p = previous_params["is_left_of_center"]           # Boolean, Flag to indicate if the agent is on the left side to the track center or not.
        is_offtrack_p = previous_params["is_offtrack"]                       # Boolean flag to indicate whether the agent has gone off track.
        is_reserved_p = previous_params["is_reversed"]                       # Boolean, flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
        heading_p = previous_params["heading"]                               # float, agent's yaw in degrees
        progress_p = previous_params["progress"]                             # float, percentage of track completed
        speed_p = previous_params["speed"]                                   # float, agent's speed in meters per second (m/s)
        steering_angle_p = previous_params["steering_angle"]                 # float, agent's steering angle in degrees
        steps_p = previous_params["steps"]                                   # int, number steps completed
        track_length_p = previous_params["track_length"]                     # float, track length in meters.
        track_width_p = previous_params["track_width"]                       # float, width of the track
        waypoints_p = previous_params["waypoints"]                           # [(float, float), list of (x,y) as milestones along the track center

        # Calculate hald width that are at varying distances away from the center line
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
            reward = reward- speed/6

        # 前回と今回のセンターから距離の差に応じて報酬を設定（蛇行運転を抑える）
        # センターラインから離れた距離を3つの段階で評価する
        marker_1 = 0.1 * track_width
        marker_2 = 0.25 * track_width
        marker_3 = 0.5 * track_width
        # 距離が大きく
        distance_diff = abs(distance_from_center-distance_from_center_p)

        if distance_diff <= marker_1:
            reward = 1.0
        elif distance_diff <= marker_2:
            reward = 0.5
        elif distance_diff <= marker_3:
            reward = 0.1

        # 100ステップごとに、予測より進捗が高かったら追加報酬を設定
        expected_steps = 300
        if (steps % 100) == 0 and progress > (steps / expected_steps) * 100:
            reward += 5.0

        # 今回のparamsをprevios_paramsにセットする
        self.previous_params = params

        return float(reward)

# Rewardクラスをインスタンス化する
reward_object = Reward()

def reward_function(params):
    return reward_object.reward_function(params)

