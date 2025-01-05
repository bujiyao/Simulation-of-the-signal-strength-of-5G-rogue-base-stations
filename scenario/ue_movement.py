import numpy as np

def generate_random_positions(num_positions, map_size):
    """
    生成隨機位置
    
    參數：
    num_positions: 位置數量
    map_size: 地圖大小
    
    回傳：
    隨機位置array，形狀為(num_positions, 2)
    """
    return np.random.rand(num_positions, 2) * map_size

def generate_waypoint(map_size):
    """
    生成單一隨機路徑點
    
    參數：
    map_size: 地圖大小
    
    回傳：
    隨機路徑點array，形狀為(2,)
    """
    return np.random.rand(2) * map_size

def simulate_ue_movement(initial_positions, speed, time, map_size, pause_time=5):
    """
    Args:
        initial_positions: 初始位置 array (NUM_UE, 2)
        speed: 移動速度
        time: 時間序列
        map_size: 地圖大小
        pause_time: 固定暫停時間，預設5秒
    """
    num_ue = initial_positions.shape[0]
    num_timesteps = len(time)
    positions = np.zeros((num_ue, num_timesteps, 2))
    positions[:, 0] = initial_positions

    current_positions = initial_positions.copy()
    waypoints = np.array([generate_waypoint(map_size) for _ in range(num_ue)])
    pause_times = np.zeros(num_ue)

    for t in range(1, num_timesteps):
        for i in range(num_ue):
            if pause_times[i] > 0:
                pause_times[i] -= time[t] - time[t-1]
                current_positions[i] = positions[i, t-1]
            else:
                direction = waypoints[i] - current_positions[i]
                distance = np.linalg.norm(direction)

                if distance < speed * (time[t] - time[t-1]):
                    current_positions[i] = waypoints[i]
                    waypoints[i] = generate_waypoint(map_size)
                    pause_times[i] = pause_time  # 固定5秒暫停
                else:
                    normalized_direction = direction / distance
                    current_positions[i] = positions[i, t-1] + normalized_direction * speed * (time[t] - time[t-1])

            positions[i, t] = current_positions[i]

    return positions