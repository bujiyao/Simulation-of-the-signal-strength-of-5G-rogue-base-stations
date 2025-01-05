import numpy as np

def calculate_Rxlev_bs(Pt_dBm, Gt_dBi, Gr_dBi, station_coords, ue_positions, wavelength):
    """
    計算接收信號強度，使用Friis方程，考慮3D距離
    
    Args:
        Pt_dBm: 發射功率(dBm)
        Gt_dBi: 發射天線增益(dBi)
        Gr_dBi: 接收天線增益(dBi)
        station_coords: 基站座標 
        ue_positions: UE位置序列
        wavelength: 波長
        
    Returns:
        信號強度矩陣
    """
    BS_HEIGHT = 6  # 基站高度6m
    UE_HEIGHT = 1  # UE高度1m

    ue_positions_reshaped = ue_positions[:, :, np.newaxis, :]
    station_coords_reshaped = station_coords[np.newaxis, np.newaxis, :, :]
    
    distances_2d = np.sqrt(((ue_positions_reshaped - station_coords_reshaped)**2).sum(axis=3))
    height_diff = BS_HEIGHT - UE_HEIGHT
    distances_3d = np.sqrt(distances_2d**2 + height_diff**2)
    
    Pt = 10**(Pt_dBm/10) / 1000
    Gt = 10**(Gt_dBi/10)
    Gr = 10**(Gr_dBi/10)
    
    # 計算接收功率
    Pr = (Pt * Gt * Gr * wavelength**2) / ((4 * np.pi * distances_3d)**2)
    x_t = np.random.uniform(0, 2, size=distances_3d.shape)
    Rxlev = 10 * np.log10(Pr * x_t) + 30
    
    return Rxlev

def calculate_Rxlev_rbs(Pt_dBm, Gt_dBi, Gr_dBi, station_coords, ue_positions, wavelength):
    """
    計算接收信號強度，使用Friis方程，考慮3D距離
    
    Args:
        Pt_dBm: 發射功率(dBm)
        Gt_dBi: 發射天線增益(dBi)
        Gr_dBi: 接收天線增益(dBi)
        station_coords: 基站座標 
        ue_positions: UE位置序列
        wavelength: 波長
        
    Returns:
        信號強度矩陣
    """
    BS_HEIGHT = 1.5  # 基站高度6m
    UE_HEIGHT = 1  # UE高度1m

    ue_positions_reshaped = ue_positions[:, :, np.newaxis, :]
    station_coords_reshaped = station_coords[np.newaxis, np.newaxis, :, :]
    
    distances_2d = np.sqrt(((ue_positions_reshaped - station_coords_reshaped)**2).sum(axis=3))
    height_diff = BS_HEIGHT - UE_HEIGHT
    distances_3d = np.sqrt(distances_2d**2 + height_diff**2)
    
    Pt = 10**(Pt_dBm/10) / 1000
    Gt = 10**(Gt_dBi/10)
    Gr = 10**(Gr_dBi/10)
    
    # 計算接收功率
    Pr = (Pt * Gt * Gr * wavelength**2) / ((4 * np.pi * distances_3d)**2)
    x_t = np.random.uniform(0, 2, size=distances_3d.shape)
    Rxlev = 10 * np.log10(Pr * x_t) + 30
    
    return Rxlev