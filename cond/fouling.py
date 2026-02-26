"""
污垢系数与清洁系数转换模块
"""


def fouling_to_clean(f, do_mm, t_mm, u_w_m2k):
    """
    把污垢系数换算成清洁系数（无量纲）

    参数:
        f: 污垢系数，m²·K/W
        do_mm: 换热管外径，mm
        t_mm: 管壁厚度，mm
        u_w_m2k: 已修正传热系数，W/(m²·K)

    返回:
        float: 清洁系数 = 1 / (1 + U·Rf·AR)
        其中 AR = 外周长 / 内周长
    """
    # 转米
    do = do_mm * 1e-3
    di = do - 2 * t_mm * 1e-3

    if di <= 0:
        raise ValueError("壁厚过大，导致内径≤0")

    # 面积比 = 外周长 / 内周长
    ar = do / di

    # 清洁系数
    return 1 / (1 + u_w_m2k * f * ar)


if __name__ == "__main__":
    rf = 0.000343
    do = 25.0
    t = 1.0
    u = 4011.55 * 1.0788 * 0.80146175
    print("清洁系数:", round(fouling_to_clean(rf, do, t, u), 4))
