import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_legitimate_bs_signal(T, Rxlev_bs, NUM_UE, NUM_BS, ax=None):
    """繪製合法基地台的信號強度圖"""
    if ax is None:
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
        
    ue_colors = plt.cm.rainbow(np.linspace(0, 1, NUM_UE))

    for ue in range(NUM_UE):
        bs_colors = plt.cm.viridis(np.linspace(0, 1, NUM_BS)) 
        for bs in range(NUM_BS):
            ax.plot(T, Rxlev_bs[ue, :, bs], color=bs_colors[bs], alpha=0.7, 
                    label=f'UE {ue+1} - BS{bs+1}' if ue == 0 else "")

    ax.set_title("RSRP from Legitimate Base Stations")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RSRP (dBm)")
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('RSRP from Legitimate Base Stations.png', bbox_inches='tight', dpi=300)

def legitimate_bs_data(T, Rxlev_bs, Rxlev_rbs, NUM_UE, NUM_BS, NUM_RBS, handover_threshold=3, plot=True):
    """
    只有legitimate_bs的情況，使用-100 dBm代表接收不到惡意基站的訊號
    處理handover並收集資料，可選擇是否繪圖
    回傳: 收集的資料集
    """
    # 準備資料集
    total_points = len(T) * NUM_UE
    num_features = 1 + 1 + NUM_BS + NUM_RBS + 1
    dataset = np.zeros((total_points, num_features))

    # 如果需要繪圖，先畫第一個圖
    if plot:
        LegitimateSignal.plot_legitimate_bs_signal(T, Rxlev_bs, NUM_UE, NUM_BS)
        
        # 創建第二個圖
        plt.figure(figsize=(12, 8))
        ax2 = plt.gca()

    row_idx = 0
    for ue in range(NUM_UE):
        current_bs = np.argmax(Rxlev_bs[ue, 0, :])
        handover_signal = []
        connected_bs = []

        signal_history = {bs: [] for bs in range(NUM_BS)}
        time_window = 10
        last_handover_time = 0
        min_time_between_handovers = 20

        # 標記第一個點
        if plot:
            ax2.annotate(f'BS{current_bs+1}',
                        (T[0], Rxlev_bs[ue, 0, current_bs]),
                        textcoords="offset points",
                        xytext=(0, 20),
                        ha='center',
                        fontsize=12,
                        color='orange',
                        weight='bold',
                        arrowprops=dict(arrowstyle="->", color='orange'))

        for t in range(len(T)):
            current_signal = Rxlev_bs[ue, t, current_bs]

            for bs in range(NUM_BS):
                signal_history[bs].append(Rxlev_bs[ue, t, bs])
                if len(signal_history[bs]) > time_window:
                    signal_history[bs].pop(0)

            if t - last_handover_time >= min_time_between_handovers:
                max_signal = current_signal
                max_bs = current_bs

                for bs in range(NUM_BS):
                    if bs != current_bs:
                        avg_current_signal = np.mean(signal_history[current_bs])
                        avg_candidate_signal = np.mean(signal_history[bs])

                        if avg_candidate_signal >= avg_current_signal + handover_threshold:
                            if avg_candidate_signal > max_signal:
                                max_signal = avg_candidate_signal
                                max_bs = bs

                if max_bs != current_bs:
                    current_bs = max_bs
                    last_handover_time = t

                    # 如果需要繪圖，添加切換標記
                    if plot:
                        ax2.annotate(f'BS{current_bs+1}',
                                    (T[t], Rxlev_bs[ue, t, current_bs]),
                                    textcoords="offset points",
                                    xytext=(0, 20),
                                    ha='center',
                                    fontsize=12,
                                    color='orange',
                                    weight='bold',
                                    arrowprops=dict(arrowstyle="->", color='orange'))

            # 收集資料
            dataset[row_idx, 0] = T[t]
            dataset[row_idx, 1] = current_bs + 1
            dataset[row_idx, 2:2+NUM_BS] = Rxlev_bs[ue, t, :]
            dataset[row_idx, 2+NUM_BS] = -100
            dataset[row_idx, -1] = 0

            # 如果需要繪圖，收集信號數據
            if plot:
                handover_signal.append(Rxlev_bs[ue, t, current_bs])

            row_idx += 1

        # 如果需要繪圖，繪製信號路徑
        if plot:
            ax2.plot(T, handover_signal, color='blue', alpha=0.7,
                    label=f'UE {ue+1} Handover Path')
            ax2.scatter(T, handover_signal, color='blue', s=2)

    # 保存資料集
    header = ['time', 'connected_bs'] + \
            [f'BS{i+1}' for i in range(NUM_BS)] + \
            ['RBS1', 'label']

    df = pd.DataFrame(dataset, columns=header)
    df.to_csv('legitimate_bs_dataset.csv', index=False)

    # 如果需要繪圖，完成第二個圖表設置
    if plot:
        ax2.set_title("legitimate_bs_RSRP")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("RSRP (dBm)")
        ax2.grid(True)
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('legitimate_bs_RSRP.png', bbox_inches='tight', dpi=300)

    return dataset