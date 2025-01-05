from config import SystemConfig
from scenario.hex_grid import *
from scenario.signal_calculation import *
from scenario.ue_movement import *
from visualization.trajectory_plot import *
from visualization.rogue_bs_signal_plot import *
import visualization.rogue_bs_signal_plot

import matplotlib.pyplot as plt

def main():
    # 初始化系統配置
    config = SystemConfig()
    params = config.get_all_params()
   
    # 執行模擬
    ue_positions = simulate_ue_movement(
        initial_positions=params['positions']['ue_initial_positions'],
        speed=params['movement']['V'],
        time=params['movement']['T'],
        map_size=params['map']['MAP_SIZE'],
        pause_time=5  # 固定5秒
    )
   
    # 計算信號強度
    Rxlev_bs = calculate_Rxlev_bs(
        Pt_dBm=params['power']['Pt_bs'],
        Gt_dBi=params['power']['Gt_bs'],
        Gr_dBi=params['power']['Gr_bs'],
        station_coords=params['positions']['bs_coords'],
        ue_positions=ue_positions,
        wavelength=params['physical']['wavelength']
    )
   
    Rxlev_rbs = calculate_Rxlev_rbs(
        Pt_dBm=params['power']['Pt_rbs'],
        Gt_dBi=params['power']['Gt_rbs'],
        Gr_dBi=params['power']['Gr_rbs'],
        station_coords=params['positions']['rbs_coords'],
        ue_positions=ue_positions,
        wavelength=params['physical']['wavelength']
    )
   
    # 繪製移動路徑圖
    plot_ue_trajectories(
        bs_coords=params['positions']['bs_coords'],
        rbs_coords=params['positions']['rbs_coords'],
        ue_positions=ue_positions,
        map_size=params['map']['MAP_SIZE'],
        radius=params['map']['radius']
    )

    # 設定攻擊時間區間
    attack_periods = [
        (3000, 3200),    # 第一次攻擊：200秒
        (3400, 3500),    # 第二次攻擊：100秒
        (3520, 3540)     # 第三次攻擊：20秒
    ]

    # 調用函數
    rogue_bs_dataset = rogue_bs_data(
        T=params['movement']['T'],
        Rxlev_bs=Rxlev_bs,
        Rxlev_rbs=Rxlev_rbs,
        NUM_UE=params['system']['NUM_UE'],
        NUM_BS=params['system']['NUM_BS'],
        NUM_RBS=params['system']['NUM_RBS'],
        attack_periods=attack_periods,
        handover_threshold=3,
        plot=True
    )
    # 顯示全部圖形
    # plt.show()
    return rogue_bs_dataset

if __name__ == "__main__":
    dataset = main()