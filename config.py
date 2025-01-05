import numpy as np
from scenario.hex_grid import *
from scenario.ue_movement import *

class SystemConfig:
    def __init__(self):
        # 物理常數
        self.c = 3 * 10**8  # 光速 (m/s)
        self.frequency = 3.5 * 10**9  # 5G New Radio 頻率 (3.5 GHz)
        self.wavelength = self.c / self.frequency  # 波長 (m)
        
        # 發射功率和天線增益
        self.Pt_bs = 23  # 合法基站發射功率 (23 dBm = 0.2 Watt)
        self.Pt_rbs = 20  # 惡意基站發射功率 (20 dBm ≈ 0.1 Watt)
        self.Gt_bs = 1  # 合法基站增益 (1 dBi)
        self.Gr_bs = 1  # 接收增益 (1 dBi)
        self.Gt_rbs = 15  # 惡意基站增益 (15 dBi)
        self.Gr_rbs = 1  # 接收增益 (1 dBi)
        
        # 移動參數
        self.V = 1  # UE平均速度 (1 m/s)
        self.T = np.linspace(0, 3600, 36001)  # 時間 (秒)，總共模擬1小時
        
        # 地圖參數
        self.MAP_SIZE = 1000  # 1000m*1000m
        
        # 系統參數
        self.NUM_BS = 7   # 7個合法基站
        self.NUM_RBS = 1  # 1個惡意基站
        self.NUM_UE = 1   # 1個UE
        
        # 初始化基站和UE位置
        self._initialize_positions()
        
    def _initialize_positions(self):
        """初始化所有位置"""
        # 中心點和半徑
        self.center_x = self.MAP_SIZE/2
        self.center_y = self.MAP_SIZE/2
        self.radius = self.MAP_SIZE/4
        
        # 生成基站位置
        bs_positions, self.cell_vertices = generate_hexagonal_grid(
            self.center_x, self.center_y, self.radius, 1)
        self.bs_coords = bs_positions[:self.NUM_BS]
        
        # 生成UE初始位置
        self.ue_initial_positions = generate_random_positions(self.NUM_UE, self.MAP_SIZE)
        
        # 設定惡意基站位置在中間偏下
        rbs_x = self.MAP_SIZE/2  # x座標在正中間
        rbs_y = self.MAP_SIZE/2 - 50  # y座標比中心點低100米
        self.rbs_coords = np.array([[rbs_x, rbs_y]])  # 形狀為 (NUM_RBS, 2)
        # self.rbs_coords = generate_random_positions(self.NUM_RBS, self.MAP_SIZE)

    def get_all_params(self):
        """返回所有系統參數"""
        return {
            'physical': {
                'c': self.c,
                'frequency': self.frequency,
                'wavelength': self.wavelength
            },
            'power': {
                'Pt_bs': self.Pt_bs,
                'Pt_rbs': self.Pt_rbs,
                'Gt_bs': self.Gt_bs,
                'Gr_bs': self.Gr_bs,
                'Gt_rbs': self.Gt_rbs,
                'Gr_rbs': self.Gr_rbs
            },
            'movement': {
                'V': self.V,
                'T': self.T
            },
            'map': {
                'MAP_SIZE': self.MAP_SIZE,
                'center_x': self.center_x,
                'center_y': self.center_y,
                'radius': self.radius
            },
            'system': {
                'NUM_BS': self.NUM_BS,
                'NUM_RBS': self.NUM_RBS,
                'NUM_UE': self.NUM_UE
            },
            'positions': {
                'bs_coords': self.bs_coords,
                'rbs_coords': self.rbs_coords,
                'ue_initial_positions': self.ue_initial_positions,
                'cell_vertices': self.cell_vertices
            }
        }