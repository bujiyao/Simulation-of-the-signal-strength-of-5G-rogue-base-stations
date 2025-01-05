import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def plot_initial_positions(bs_coords, rbs_coords, ue_initial_positions, map_size, radius):
    """
    繪製初始位置圖，包含基站、惡意基站和UE的位置
    """
    plt.figure(figsize=(10, 10))

    # 繪製基站覆蓋範圍
    for idx, pos in enumerate(bs_coords[:7]):
        circle = Circle(pos, radius, facecolor='none', edgecolor='blue', alpha=0.5)
        plt.gca().add_patch(circle)
        plt.text(pos[0], pos[1] + radius * 0.05, f'BS{idx+1}', 
                ha='center', va='bottom', color='blue', 
                fontsize=10, weight='bold')

    # 繪製基站位置
    plt.scatter(bs_coords[:, 0], bs_coords[:, 1], 
                c='blue', s=100, label='Legitimate BS')
    plt.scatter(rbs_coords[:, 0], rbs_coords[:, 1], 
                c='red', s=100, marker='s', label='Malicious BS')

    # 繪製UE初始位置
    for ue in range(len(ue_initial_positions)):
        plt.scatter(ue_initial_positions[ue, 0], ue_initial_positions[ue, 1],
                    color=plt.cm.rainbow(ue / len(ue_initial_positions)),
                    s=50, marker='*', label=f'UE {ue+1} start')

    plt.title("Base Station Locations and Initial UE Positions")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.axis('equal')
    plt.plot([0, map_size, map_size, 0, 0], [0, 0, map_size, map_size, 0], 
            'k--', label='Map Boundary')
    plt.tight_layout()