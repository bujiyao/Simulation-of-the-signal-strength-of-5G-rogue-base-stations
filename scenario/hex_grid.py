import numpy as np

def generate_hex_vertices(center_x, center_y, radius):
    """
    生成單個六邊形的六個頂點座標。
    
    Args:
        center_x (float): 六邊形中心的 X 座標。
        center_y (float): 六邊形中心的 Y 座標。
        radius (float): 六邊形外接圓半徑。
        
    Returns:
        np.ndarray: 六邊形的頂點座標 (6, 2)。
    """
    angles_rad = np.linspace(0, 2 * np.pi, 7)[:-1]
    vertices = np.array([
        (center_x + radius * np.cos(angle), center_y + radius * np.sin(angle))
        for angle in angles_rad
    ])
    return vertices

def generate_hexagonal_grid(center_x, center_y, radius, layers):
    """
    生成多層六邊形基站的佈局，包含中心基站和周圍基站。

    Args:
        center_x (float): 網格中心基站的 X 座標。
        center_y (float): 網格中心基站的 Y 座標。
        radius (float): 每個六邊形的半徑。
        layers (int): 包含的六邊形層數。
        
    Returns:
        tuple:
            - np.ndarray: 所有基站中心座標 (N, 2)。
            - list[np.ndarray]: 每個基站對應的六邊形頂點座標。
    """
    positions = [(center_x, center_y)] 
    cell_vertices = [generate_hex_vertices(center_x, center_y, radius)] 

    for layer in range(1, layers + 1):
        for side in range(6): 
            angle_deg = 60 * side
            angle_rad = np.deg2rad(angle_deg)

            start_x = center_x + layer * radius * np.sqrt(3) * np.cos(angle_rad)
            start_y = center_y + layer * radius * np.sqrt(3) * np.sin(angle_rad)
            
            for pos in range(layer):
                dx = radius * np.sqrt(3) * np.cos(angle_rad + np.pi / 3)
                dy = radius * np.sqrt(3) * np.sin(angle_rad + np.pi / 3)

                bs_x = start_x - pos * dx
                bs_y = start_y - pos * dy

                positions.append((bs_x, bs_y))
                cell_vertices.append(generate_hex_vertices(bs_x, bs_y, radius))

    return np.array(positions), cell_vertices