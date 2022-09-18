def reward_function(params):
    '''
    デフォルトで設定させている報酬の例
    [メモ]
    エージェントは報酬の中身を理解していない。
    インプットされる情報は、カメラで撮影された画像のみ。
    画像をもとにエージェントが行動を決定する。
    行動した結果、以下に報酬関数に沿って報酬が与えられる。
    '''

    # paramsの読み出し
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

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

    return float(reward)
