"""
换热管结构计算模块
"""
import math

# 单位转换常量
M3_H_TO_M3_S = 1 / 3600


def calc_tube_velocity(vol_flow_m3_h, tube_od_mm, wall_thickness_mm, tube_count, passes=1):
    """
    计算换热管内流速（m/s）

    参数:
        vol_flow_m3_h: 冷却水体积流量 (m³/h)
        tube_od_mm: 换热管外径 (mm)
        wall_thickness_mm: 管壁厚度 (mm)
        tube_count: 换热管数量 (根)
        passes: 流程数，默认1
    返回:
        float: 管内流速 (m/s)，保留4位小数
    """
    # 类型 + 数值校验
    try:
        vol_flow_m3_h = float(vol_flow_m3_h)
        tube_od_mm = float(tube_od_mm)
        wall_thickness_mm = float(wall_thickness_mm)
        tube_count = int(tube_count)
        passes = int(passes)
    except (TypeError, ValueError):
        raise ValueError("输入类型错误")

    if vol_flow_m3_h <= 0:
        raise ValueError(f"体积流量必须>0")
    if wall_thickness_mm <= 0:
        raise ValueError(f"管壁厚度必须>0")
    if tube_od_mm <= 2 * wall_thickness_mm:
        raise ValueError(f"外径必须大于2倍壁厚")
    if tube_count < 1:
        raise ValueError(f"管数必须≥1")
    if passes < 1:
        raise ValueError(f"流程数必须≥1")

    # 单位转换
    Q_m3_s = vol_flow_m3_h * M3_H_TO_M3_S
    Di_m = (tube_od_mm - 2 * wall_thickness_mm) * 1e-3

    # 截面积计算
    Ai_single = math.pi * (Di_m / 2) ** 2
    Ai_total = Ai_single * tube_count / passes

    # 流速计算
    velocity = Q_m3_s / Ai_total if Ai_total > 0 else 0.0
    return round(velocity, 4)


def calc_tube_count_from_flow(vol_flow_m3_h, target_velocity_mps, tube_od_mm, wall_thickness_mm, passes=1):
    """
    由冷却水体积流量+目标流速 -> 所需最少换热管数量（向上取整）

    参数:
        vol_flow_m3_h: 体积流量 (m³/h)
        target_velocity_mps: 目标流速 (m/s)
        tube_od_mm: 换热管外径 (mm)
        wall_thickness_mm: 管壁厚度 (mm)
        passes: 流程数，默认1
    返回:
        int: 换热管数量（≥1）
    """
    # 类型 + 数值校验
    try:
        vol_flow_m3_h = float(vol_flow_m3_h)
        target_velocity_mps = float(target_velocity_mps)
        tube_od_mm = float(tube_od_mm)
        wall_thickness_mm = float(wall_thickness_mm)
        passes = int(passes)
    except (TypeError, ValueError):
        raise ValueError("输入类型错误")

    if vol_flow_m3_h <= 0:
        raise ValueError(f"体积流量必须>0")
    if target_velocity_mps <= 0:
        raise ValueError(f"目标流速必须>0")
    if wall_thickness_mm <= 0:
        raise ValueError(f"管壁厚度必须>0")
    if tube_od_mm <= 2 * wall_thickness_mm:
        raise ValueError(f"外径必须大于2倍壁厚")
    if passes < 1:
        raise ValueError(f"流程数必须≥1")

    # 单位转换
    vol_flow_m3_s = vol_flow_m3_h * M3_H_TO_M3_S
    Di_m = (tube_od_mm - 2 * wall_thickness_mm) * 1e-3

    # 截面积计算
    Ai_single = math.pi * (Di_m / 2) ** 2
    Ai_needed = vol_flow_m3_s / target_velocity_mps

    # 管数计算
    tube_count = math.ceil(Ai_needed / Ai_single * passes)
    return max(tube_count, 1)


def calc_tube_length_from_area(total_area_m2, tube_count, tube_od_mm):
    """
    由总换热面积+管数 -> 单根管长

    参数:
        total_area_m2: 总换热面积 (m²)
        tube_count: 换热管数量 (根)
        tube_od_mm: 换热管外径 (mm)
    返回:
        float: 单根管长 (mm)，≥1mm
    """
    # 类型 + 数值校验
    try:
        total_area_m2 = float(total_area_m2)
        tube_count = int(tube_count)
        tube_od_mm = float(tube_od_mm)
    except (TypeError, ValueError):
        raise ValueError("输入类型错误")

    if total_area_m2 <= 0:
        raise ValueError(f"总换热面积必须>0")
    if tube_count < 1:
        raise ValueError(f"管数必须≥1")
    if tube_od_mm <= 0:
        raise ValueError(f"外径必须>0")

    # 单位转换
    Do_m = tube_od_mm * 1e-3

    # 管长计算
    L_m = total_area_m2 / (math.pi * Do_m * tube_count)
    L_mm = math.floor(L_m * 1000)

    return max(1.0, L_mm)


def calculate_pipe_inner_diameter(water_mass_flow_kg_s, min_velocity_mps, max_velocity_mps, fluid_density_kg_m3=1000.0):
    """
    计算管道内径（按50mm向上圆整）

    参数:
        water_mass_flow_kg_s: 水的质量流量 (kg/s)
        min_velocity_mps: 最小允许流速 (m/s)
        max_velocity_mps: 最大允许流速 (m/s)
        fluid_density_kg_m3: 流体密度 (kg/m³)，默认1000
    返回:
        int: 圆整后的管道内径（mm）
    """
    # 参数校验
    if water_mass_flow_kg_s <= 0:
        raise ValueError(f"质量流量必须>0")
    if min_velocity_mps <= 0:
        raise ValueError(f"最小流速必须>0")
    if max_velocity_mps <= min_velocity_mps:
        raise ValueError(f"最大流速必须大于最小流速")
    if fluid_density_kg_m3 <= 0:
        raise ValueError(f"流体密度必须>0")

    # 质量流量 -> 体积流量
    water_vol_flow_m3_s = water_mass_flow_kg_s / fluid_density_kg_m3

    # 计算管道内径
    inner_diameter_m = math.sqrt((4 * water_vol_flow_m3_s) / (math.pi * max_velocity_mps))
    inner_diameter_mm = inner_diameter_m * 1000

    # 按50mm向上圆整
    rounded_diameter_mm = math.ceil(inner_diameter_mm / 50) * 50

    return int(rounded_diameter_mm)


if __name__ == "__main__":
    # 测试
    v = calc_tube_velocity(100, 25, 1, 1000, 2)
    print(f"流速: {v} m/s")
    
    n = calc_tube_count_from_flow(100, 2.0, 25, 1, 2)
    print(f"管数: {n}")
    
    l = calc_tube_length_from_area(1000, 1000, 25)
    print(f"管长: {l} mm")
    
    d = calculate_pipe_inner_diameter(20 * 3.6, 0.5, 1)
    print(f"接管直径: {d} mm")
