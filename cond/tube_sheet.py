"""
管板直径计算模块
"""
import math


def calculate_tube_sheet_diameter(tube_diameter, tube_count, flow_number, tube_spacing):
    """
    计算换热管板外径（工程实用估算公式）

    参数:
        tube_diameter: 换热管的外径 (mm)
        tube_count: 换热管的数量 (根)
        flow_number: 流程数
        tube_spacing: 换热管的中心间距 (mm)
    返回:
        float: 管板外径 (mm)
    """
    # 参数校验
    if tube_diameter <= 0:
        raise ValueError(f"换热管外径必须>0")
    if tube_count < 1:
        raise ValueError(f"换热管数量必须≥1")
    if flow_number < 1:
        raise ValueError(f"流程数必须≥1")
    if tube_spacing <= tube_diameter:
        raise ValueError(f"管间距必须大于管外径")

    # 计算
    intermediate_result = tube_count / 0.6
    sqrt_result = math.sqrt(intermediate_result)
    adjustment_factor = 1 + 0.05 * flow_number
    tube_sheet_diameter = sqrt_result * adjustment_factor * tube_spacing

    return tube_sheet_diameter


if __name__ == "__main__":
    d = calculate_tube_sheet_diameter(25, 6750, 4, 32)
    print(f"管板外径: {d:.2f} mm")
