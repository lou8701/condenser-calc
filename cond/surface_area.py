"""
换热面积计算模块
"""


def heat_transfer_area(heat_load, lmtd, u_uncorrect, fw_water, fw_mat, fouling_factor=1.0):
    """
    计算换热面积 A (m²)
    公式：A = Q / (LMTD × U × fw_water × fw_mat × fouling_factor)

    参数:
        heat_load: 热负荷 (kW)，必须>0
        lmtd: 对数平均温差 (°C)，必须>0
        u_uncorrect: 未修正传热系数 (W/(m²·K))，必须>0
        fw_water: 水温修正系数，必须>0
        fw_mat: 材料修正系数，必须>0
        fouling_factor: 清洁系数，默认1.0，必须>0
    返回:
        float: 换热面积 (m²)，保留2位小数
    """
    # 输入校验
    if heat_load <= 0:
        raise ValueError(f"热负荷({heat_load} kW)必须>0")
    if lmtd <= 0:
        raise ValueError(f"对数平均温差({lmtd} °C)必须>0")
    if u_uncorrect <= 0:
        raise ValueError(f"未修正传热系数({u_uncorrect})必须>0")
    if fw_water <= 0:
        raise ValueError(f"水温修正系数({fw_water})必须>0")
    if fw_mat <= 0:
        raise ValueError(f"材料修正系数({fw_mat})必须>0")
    if fouling_factor <= 0:
        raise ValueError(f"清洁系数({fouling_factor})必须>0")

    # 核心计算（1000转换：kW -> W）
    area = 1000 * heat_load / (lmtd * u_uncorrect * fw_water * fw_mat * fouling_factor)
    return round(area, 2)


if __name__ == "__main__":
    print(heat_transfer_area(1000, 10, 4000, 1.0, 0.9, 0.85))
