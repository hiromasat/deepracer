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
        # params
        all_wheels_on_track = params["all_wheels_on_track"],      # flag to indicate if the agent is on the track
        x = params["x"]                                           # float, agent's x-coordinate in meters
        y = params["y"]                                           # float, agent's y-coordinate in meters
        closest_waypoints = params["closest_waypoints"]           # [int, int], indices of the two nearest waypoints.
        distance_from_center = params["distance_from_center"]     # float, distance in meters from the track center
        is_crashed = params["is_crashed"]                         # Boolean flag to indicate whether the agent has crashed.
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
        all_wheels_on_track = previous_params["all_wheels_on_track"],      # flag to indicate if the agent is on the track
        x = previous_params["x"]                                           # float, agent's x-coordinate in meters
        y = previous_params["y"]                                           # float, agent's y-coordinate in meters
        closest_waypoints = previous_params["closest_waypoints"]           # [int, int], indices of the two nearest waypoints.
        distance_from_center = previous_params["distance_from_center"]     # float, distance in meters from the track center
        is_crashed = previous_params["is_crashed"]                         # Boolean flag to indicate whether the agent has crashed.
        is_left_of_center = previous_params["is_left_of_center"]           # Boolean, Flag to indicate if the agent is on the left side to the track center or not.
        is_offtrack = previous_params["is_offtrack"]                       # Boolean flag to indicate whether the agent has gone off track.
        is_reserved = previous_params["is_reversed"]                       # Boolean, flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
        heading = previous_params["heading"]                               # float, agent's yaw in degrees
        progress = previous_params["progress"]                             # float, percentage of track completed
        speed = previous_params["speed"]                                   # float, agent's speed in meters per second (m/s)
        steering_angle = previous_params["steering_angle"]                 # float, agent's steering angle in degrees
        steps = previous_params["steps"]                                   # int, number steps completed
        track_length = previous_params["track_length"]                     # float, track length in meters.
        track_width = previous_params["track_width"]                       # float, width of the track
        waypoints = previous_params["waypoints"]                           # [(float, float), list of (x,y) as milestones along the track center

        previous_params = params


        # Calculate hald width that are at varying distances away from the center line
        prev_point = waypoints[closest_waypoints[0]]
        ext_point = waypoints[closest_waypoints[1]]
        # Track direction
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        # Convert to degree
        track_direction = math.degrees(track_direction)

        if track_direction < 0:
            track_direction += 360
            reward = 1e-3

        # Give minimal reward if not on track
        if not all_wheels_on_track:
            reward = 1e-3
        else:
            # Reward for higher speed
            reward = reward + speed / 6
            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = track_direction - heading
            # Effective angle difference
            direction_diff = (direction_diff + 180) % 360 - 180
            # Penalize the reward if the difference is too large
            reward = reward + 1 - direction_diff / 90
            if direction_diff <= 12 and steering_angle == 0:
                reward += 1
            # if difference between direction-heading angle and steering_angle is large, penalize
            elif abs(direction_diff) > 12:
                reward = reward + 1 - abs(direction_diff - steering_angle) / 30
            # Penalize high steering_angle
            reward = reward + 1 - abs(steering_angle) / 24
            expected_steps = 300
            if (steps % 100) == 0 and progress > (steps / expected_steps) * 100:
                reward += 5.0

        # 今回のparamsをprevios_paramsにセットする
        self.previous_params = params
        return float(reward)


reward_object = Reward()

def reward_function(params):
    return reward_object.reward_function(params)
