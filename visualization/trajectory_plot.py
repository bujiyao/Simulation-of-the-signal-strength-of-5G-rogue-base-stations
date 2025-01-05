import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

def plot_ue_trajectories(bs_coords, rbs_coords, ue_positions, map_size, radius):
    """
    繪製 UE 的移動軌跡，包括合法基站和偽基站的位置。

    Args:
        bs_coords (np.ndarray): 合法基站的座標 (N, 2)。
        rbs_coords (np.ndarray): 偽基站的座標 (M, 2)。
        ue_positions (np.ndarray): UE 的移動軌跡 (K, T, 2)，K 表示 UE 數量，T 表示時間步長。
        map_size (float): 地圖大小（正方形邊長）。
        radius (float): 基站的覆蓋半徑。
    """
    plt.figure(figsize=(10, 10))

    # 繪製合法基站的覆蓋範圍及標籤
    for idx, pos in enumerate(bs_coords[:7]):  # 只標記前 7 個合法基站
        circle = Circle(pos, radius, facecolor='none', edgecolor='gray', alpha=0.5)
        plt.gca().add_patch(circle)
        plt.text(pos[0], pos[1] + radius * 0.05, f'BS{idx+1}', ha='center', va='bottom', color='blue', fontsize=10, weight='bold')

    # 繪製基站位置
    plt.scatter(bs_coords[:, 0], bs_coords[:, 1], c='blue', s=100, label='Legitimate BS')
    plt.scatter(rbs_coords[:, 0], rbs_coords[:, 1], c='red', s=100, marker='s', label='Rogue BS')

    # 繪製 UE 的移動軌跡
    for ue in range(len(ue_positions)):
        color = plt.cm.rainbow(ue / len(ue_positions))
        plt.plot(ue_positions[ue, :, 0], ue_positions[ue, :, 1], color=color, alpha=0.5, label=f'UE {ue+1} path')
        plt.scatter(ue_positions[ue, 0, 0], ue_positions[ue, 0, 1], color=color, s=100, marker='o',
                edgecolor='black', linewidth=2, label=f'UE {ue+1} start')

    # 設置圖形屬性
    plt.title("UE Movement Trajectories")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.axis('equal')
    # 繪製地圖邊界
    plt.plot([0, map_size, map_size, 0, 0], [0, 0, map_size, map_size, 0], 'k--', label='Map Boundary')
    plt.tight_layout()
    plt.savefig('result/UE_Movement_Trajectories.png', bbox_inches='tight', dpi=300)
