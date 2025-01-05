import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

def plot_all_bs_signal(T, Rxlev_bs, Rxlev_rbs, NUM_UE, NUM_BS, NUM_RBS):
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 為每個UE設置顏色
    ue_colors = plt.cm.rainbow(np.linspace(0, 1, NUM_UE))
    bs_colors = plt.cm.viridis(np.linspace(0, 1, NUM_BS))  # 合法基站用綠色系
    rbs_colors = plt.cm.Reds(np.linspace(0.3, 1, NUM_RBS))  # 惡意基站用紅色系

    # 遍歷每個UE
    for ue in range(NUM_UE):
        # 繪製合法基站信號
        for bs in range(NUM_BS):
            ax.plot(T, Rxlev_bs[ue, :, bs],
                    color=bs_colors[bs],
                    alpha=0.7,
                    label=f'BS{bs+1}')

        # 繪製惡意基站信號
        for rbs in range(NUM_RBS):
            ax.plot(T, Rxlev_rbs[ue, :, rbs],
                    color=rbs_colors[rbs],
                    alpha=0.7,
                    linestyle='--',
                    label=f'RBS{rbs+1}')

    ax.set_title("RSRP from All Base Stations")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RSRP (dBm)")
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('result/RSRP_from_All_Base_Stations.png', bbox_inches='tight', dpi=300)

def rogue_bs_data(T, Rxlev_bs, Rxlev_rbs, NUM_UE, NUM_BS, NUM_RBS, attack_periods=None, handover_threshold=3, plot=True):
    """
    產生多次攻擊的惡意基地台數據
    
    Args:
        T: 時間序列
        Rxlev_bs: 合法基站信號強度
        Rxlev_rbs: 惡意基站信號強度
        NUM_UE: UE數量
        NUM_BS: 合法基站數量
        NUM_RBS: 惡意基站數量
        attack_periods: 攻擊時間區間列表，例如: [(1201, 1320), (4201, 4320)]
        handover_threshold: 切換閾值
        plot: 是否繪圖
    """
    # 準備資料集
    total_points = len(T) * NUM_UE
    num_features = 1 + 1 + NUM_BS + NUM_RBS + 1
    dataset = np.zeros((total_points, num_features))

    # 產生攻擊區間的RBS信號
    attack_rbs = np.ones_like(Rxlev_rbs) * -100  # 初始化為-100dBm

    # 確保攻擊時間在範圍內
    if attack_periods is not None:
        attack_periods = [(start, min(end, T[-1])) for start, end in attack_periods if start < T[-1]]
        
        # 在指定的攻擊時間區間設定RBS信號
        for start_time, end_time in attack_periods:
            start_idx = np.where(T >= start_time)[0][0]
            end_idx = np.where(T >= end_time)[0][0] if end_time < T[-1] else len(T)
            attack_rbs[:, start_idx:end_idx, :] = Rxlev_rbs[:, start_idx:end_idx, :]

    if plot:
        # 畫第一張圖：所有基地台信號
        plot_all_bs_signal(T, Rxlev_bs, Rxlev_rbs, NUM_UE, NUM_BS, NUM_RBS)
        
        # 創建第二張圖：切換情況
        plt.figure(figsize=(12, 8))
        ax2 = plt.gca()
        
        # 標示攻擊區間
        if attack_periods is not None:
            first_attack = True
            ymin, ymax = -100, -30  # 設定固定的y軸範圍
            for start_time, end_time in attack_periods:
                ax2.axvspan(start_time, end_time, 
                            color='red', alpha=0.1,
                            label='Attack Period' if first_attack else None)
                ax2.text((start_time + end_time)/2, ymax, 
                        f'Attack\n{end_time-start_time}s',
                        horizontalalignment='center',
                        verticalalignment='top')
                first_attack = False

    row_idx = 0
    for ue in range(NUM_UE):
        # 初始化：選擇信號最強的基站
        all_signals_initial = np.concatenate([Rxlev_bs[ue, 0, :], attack_rbs[ue, 0, :]])
        current_bs = np.argmax(all_signals_initial)
        is_rogue = current_bs >= NUM_BS

        # 追蹤信號
        handover_signal = [all_signals_initial[current_bs]]
        bs_type = ['rogue' if is_rogue else 'Legitimate']

        # 第一個點標記
        if plot:
            bs_name = f'RBS{current_bs-NUM_BS+1}' if is_rogue else f'BS{current_bs+1}'
            color = 'purple' if is_rogue else 'orange'
            ax2.annotate(bs_name,
                        (T[0], all_signals_initial[current_bs]),
                        textcoords="offset points",
                        xytext=(0, 20),
                        ha='center',
                        fontsize=12,
                        color=color,
                        weight='bold',
                        arrowprops=dict(arrowstyle="->", color=color))

        signal_history = {bs: [] for bs in range(NUM_BS + NUM_RBS)}
        time_window = 10
        last_handover_time = 0
        min_time_between_handovers = 20
        
        # 儲存第一個時間點的數據
        dataset[row_idx] = [T[0], current_bs + 1] + \
                        list(Rxlev_bs[ue, 0, :]) + \
                        [attack_rbs[ue, 0, 0]] + \
                        [1 if is_rogue else 0]
        row_idx += 1

        # 處理剩餘時間點
        for t in range(1, len(T)):
            all_signals = np.concatenate([Rxlev_bs[ue, t, :], attack_rbs[ue, t, :]])
            current_signal = all_signals[current_bs]

            # 更新信號歷史
            for bs in range(NUM_BS + NUM_RBS):
                signal_history[bs].append(all_signals[bs])
                if len(signal_history[bs]) > time_window:
                    signal_history[bs].pop(0)

            # 檢查是否需要切換基站
            if t - last_handover_time >= min_time_between_handovers:
                max_signal = current_signal
                max_bs = current_bs

                for bs in range(NUM_BS + NUM_RBS):
                    if bs != current_bs:
                        avg_current_signal = np.mean(signal_history[current_bs])
                        avg_candidate_signal = np.mean(signal_history[bs])

                        if avg_candidate_signal >= avg_current_signal + handover_threshold:
                            if avg_candidate_signal > max_signal:
                                max_signal = avg_candidate_signal
                                max_bs = bs

                if max_bs != current_bs:
                    current_bs = max_bs
                    is_rogue = current_bs >= NUM_BS
                    last_handover_time = t

                    if plot:
                        bs_name = f'RBS{current_bs-NUM_BS+1}' if is_rogue else f'BS{current_bs+1}'
                        color = 'purple' if is_rogue else 'orange'
                        ax2.annotate(bs_name,
                                (T[t], all_signals[current_bs]),
                                textcoords="offset points",
                                xytext=(0, 20),
                                ha='center',
                                fontsize=12,
                                color=color,
                                weight='bold',
                                arrowprops=dict(arrowstyle="->", color=color))

            handover_signal.append(all_signals[current_bs])
            bs_type.append('rogue' if is_rogue else 'Legitimate')

            # 儲存數據
            dataset[row_idx] = [T[t], current_bs + 1] + \
                            list(Rxlev_bs[ue, t, :]) + \
                            [attack_rbs[ue, t, 0]] + \
                            [1 if is_rogue else 0]
            row_idx += 1

        if plot:
            # 繪製連接線和散點
            for i in range(1, len(T)):
                color = 'red' if bs_type[i] == 'rogue' else 'blue'
                linestyle = '--' if bs_type[i] == 'rogue' else '-'
                ax2.plot([T[i-1], T[i]], 
                        [handover_signal[i-1], handover_signal[i]],
                        color=color, linestyle=linestyle, alpha=0.7)

            ax2.scatter(T, handover_signal,
                    c=['red' if t == 'rogue' else 'blue' for t in bs_type],
                    s=2, alpha=0.5)

    # 儲存數據集
    header = ['time', 'connected_bs'] + \
            [f'BS{i+1}' for i in range(NUM_BS)] + \
            ['RBS1', 'label']
    
    df = pd.DataFrame(dataset, columns=header)
    df.to_csv('result/rogue_bs_dataset.csv', index=False)

    if plot:
        # 設定圖表屬性
        ax2.set_title("Multiple Rogue BS Attacks RSRP")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("RSRP (dBm)")
        ax2.grid(True)

        # 添加圖例
        legend_elements = [
            Line2D([0], [0], color='blue', label='Legitimate BS', alpha=0.7),
            Line2D([0], [0], color='red', linestyle='--', label='Rogue BS', alpha=0.7),
            mpatches.Patch(color='red', alpha=0.1, label='Attack Period')
        ]
        ax2.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig('result/Multiple_Rogue_bs_attacks_RSRP.png', bbox_inches='tight', dpi=300)

    return dataset