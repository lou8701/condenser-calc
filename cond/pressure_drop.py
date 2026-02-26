"""
HEI标准凝汽器水阻计算模块
"""


# 简化版HEI水阻计算（基于公式）
def calculate_hei_water_resistance(di_mm, velocity_ms, length_mm, passes, temp_c):
    """
    HEI标准凝汽器水阻计算函数（简化版）

    参数:
        di_mm: 管内径 (mm)
        velocity_ms: 流速 (m/s)
        length_mm: 管长 (mm)
        passes: 流程数 (1, 2, 或 4)
        temp_c: 冷却水平均温度 (°C)
    返回:
        float: 水阻 (kPa)
    """
    # 参数校验
    if di_mm <= 0:
        raise ValueError("管内径必须>0")
    if velocity_ms <= 0:
        raise ValueError("流速必须>0")
    if length_mm <= 0:
        raise ValueError("管长必须>0")
    if passes not in [1, 2, 4]:
        raise ValueError("流程数必须是1、2或4")

    # 单位转换
    di_m = di_mm / 1000.0
    length_m = length_mm / 1000.0

    # 单位长度阻力 dPL (公式: dPL = 28.72 * v^1.75 / di^1.25)
    dpl = 28.72 * (velocity_ms ** 1.75) / (di_m ** 1.25)

    # 温度修正系数 Rt (简化计算)
    # 基于HEI标准的简化公式
    rt = 1.0 - 0.002 * (temp_c - 20)  # 20°C为基准温度
    rt = max(0.9, min(1.1, rt))  # 限制在合理范围

    # 管内总摩擦阻力 dPa
    total_length_m = length_m * passes
    dpa = total_length_m * dpl * rt

    # 局部阻力 (端部、进出口) - 简化估算
    # 基于流程数和流速的经验公式
    pb = 0.5 * (velocity_ms ** 2) * passes * 0.1  # 端部阻力
    pc = 0.3 * (velocity_ms ** 2) * passes * 0.1  # 进出口阻力
    pd = 0.2 * (velocity_ms ** 2) * passes * 0.1  # 其他局部阻力

    # 总水阻 dPw
    dpw = dpa + pb + pc + pd
    return round(dpw, 7)


if __name__ == "__main__":
    res = calculate_hei_water_resistance(di_mm=23.6, velocity_ms=2.1, length_mm=12800, passes=2, temp_c=38.5)
    print(f"水阻: {res} kPa")
