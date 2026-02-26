"""
传热系数计算模块
"""

# 直径 mm -> 各流速对应 U 值 (Btu/(h·ft²·°F))
_RAW = {
    15.875: [462.5, 499.5, 534.0, 566.4, 597.0, 626.2, 654.0, 680.7, 706.4, 731.2, 755.2, 775.5, 795.3, 814.1, 831.9,
             848.9, 865.2, 880.7, 895.6],
    19.050: [462.5, 499.5, 534.0, 566.4, 597.0, 626.2, 654.0, 680.7, 706.4, 731.2, 755.2, 775.5, 795.3, 814.1, 831.9,
             848.9, 865.2, 880.7, 895.6],
    22.225: [455.0, 492.0, 526.0, 557.9, 588.1, 616.8, 644.2, 670.5, 695.8, 720.3, 743.9, 763.9, 783.2, 801.6, 819.0,
             835.6, 851.5, 866.6, 881.1],
    25.400: [455.0, 492.0, 526.0, 557.9, 588.1, 616.8, 644.2, 670.5, 695.8, 720.3, 743.9, 763.9, 783.2, 801.6, 819.0,
             835.6, 851.5, 866.6, 881.1],
    28.575: [448.6, 484.5, 518.0, 549.4, 579.1, 607.4, 634.4, 660.3, 685.2, 709.3, 732.6, 752.0, 770.7, 788.4, 805.3,
             821.4, 836.7, 851.3, 865.3],
    31.750: [448.6, 484.5, 518.0, 549.4, 579.1, 607.4, 634.4, 660.3, 685.2, 709.3, 732.6, 752.0, 770.7, 788.4, 805.3,
             821.4, 836.7, 851.3, 865.3],
    34.925: [441.7, 477.1, 510.0, 540.9, 570.2, 598.0, 624.6, 650.1, 674.7, 698.3, 721.2, 740.4, 758.7, 776.1, 792.6,
             808.3, 823.2, 837.5, 851.2],
    38.100: [441.7, 477.1, 510.0, 540.9, 570.2, 598.0, 624.6, 650.1, 674.7, 698.3, 721.2, 740.4, 758.7, 776.1, 792.6,
             808.3, 823.2, 837.5, 851.2],
    41.275: [434.7, 469.6, 502.0, 532.5, 561.3, 588.6, 614.8, 639.9, 664.1, 687.4, 709.9, 727.8, 745.7, 762.7, 778.8,
             794.1, 808.8, 822.7, 836.0],
    44.450: [434.7, 469.6, 502.0, 532.5, 561.3, 588.6, 614.8, 639.9, 664.1, 687.4, 709.9, 727.8, 745.7, 762.7, 778.8,
             794.1, 808.8, 822.7, 836.0],
    47.625: [427.8, 462.1, 494.0, 524.0, 552.3, 579.8, 605.0, 629.7, 653.5, 676.4, 698.6, 716.8, 734.4, 751.0, 766.8,
             781.8, 796.2, 809.8, 822.9],
    50.800: [427.8, 462.1, 494.0, 524.0, 552.3, 579.8, 605.0, 629.7, 653.5, 676.4, 698.6, 716.8, 734.4, 751.0, 766.8,
             781.8, 796.2, 809.8, 822.9],
}

_VELOCITIES = [3.0 + 0.5 * i for i in range(19)]  # 3.0-12.0 ft/s
_DIAMETERS = list(_RAW.keys())
MPS_TO_FPS = 1 / 0.3048
FPS_TO_MPS = 0.3048
_MIN_DIAM = min(_DIAMETERS)
_MAX_DIAM = max(_DIAMETERS)
_MIN_VEL_FPS = min(_VELOCITIES)
_MAX_VEL_FPS = max(_VELOCITIES)
_MIN_VEL_MPS = round(FPS_TO_MPS * _MIN_VEL_FPS, 2)
_MAX_VEL_MPS = round(FPS_TO_MPS * _MAX_VEL_FPS, 2)


def mps2fps(v):
    """m/s -> ft/s"""
    return v * MPS_TO_FPS


def _linear_interp(x, x_list, y_list):
    """线性插值"""
    if x <= x_list[0]:
        return y_list[0]
    if x >= x_list[-1]:
        return y_list[-1]
    
    for i in range(len(x_list) - 1):
        if x_list[i] <= x <= x_list[i + 1]:
            t = (x - x_list[i]) / (x_list[i + 1] - x_list[i])
            return y_list[i] + t * (y_list[i + 1] - y_list[i])
    return y_list[-1]


def uncorrected_u(diameter_mm, velocity):
    """
    根据换热管外径(mm)与管内水流速(m/s) -> 未修正传热系数 U (Btu/(h·ft²·°F))

    参数:
        diameter_mm: 换热管外径 (mm)，范围 [15.875, 50.800]
        velocity: 管内水流速 (m/s)，范围 [0.91, 3.66]
    返回:
        float: 未修正传热系数 U (Btu/(h·ft²·°F))，保留1位小数
    """
    # 类型校验
    try:
        diameter_mm = float(diameter_mm)
        velocity = float(velocity)
    except (TypeError, ValueError):
        raise ValueError("管径和流速必须为数字类型")

    # 范围校验
    if not (_MIN_DIAM <= diameter_mm <= _MAX_DIAM):
        raise ValueError(f"管径超出范围！允许范围：[{_MIN_DIAM}, {_MAX_DIAM}] mm")

    velocity_fps = mps2fps(velocity)
    if not (_MIN_VEL_FPS <= velocity_fps <= _MAX_VEL_FPS):
        raise ValueError(f"流速超出范围！m/s范围：[{_MIN_VEL_MPS}, {_MAX_VEL_MPS}]")

    # 对直径方向插值
    u_vs_v = []
    for i in range(len(_VELOCITIES)):
        u_at_v = _linear_interp(diameter_mm, _DIAMETERS, [_RAW[d][i] for d in _DIAMETERS])
        u_vs_v.append(u_at_v)

    # 对流速方向插值
    u = _linear_interp(velocity_fps, _VELOCITIES, u_vs_v)
    return round(u, 1)


if __name__ == "__main__":
    print(uncorrected_u(30, 2.2))
