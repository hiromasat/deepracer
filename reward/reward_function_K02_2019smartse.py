def reward_function(params):
     import math
     '''
     Input: dict type
     Document: https://docs.aws.amazon.com/ja_jp/deepracer/latest/developerguide/deepracer-reward-function-input.html?icmpid=docs_deepracer_console
     '''
     # Read input parameters
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

     # トラックから外れた場合に最小の報酬を設定する
     if not all_wheels_on_track:
          reward = 1e-3
     else:
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

          # Total num of steps we want the car to finish the lap, it will vary depends on the track length
          # Give additional reward if the car pass every 100 steps faster than expected
          expected_steps = 300
          if (steps % 100) == 0 and progress > (steps / expected_steps) * 100:
               reward += 5.0
     return float(reward)
