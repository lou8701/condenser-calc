"""
对数平均温差(LMTD)计算模块
"""
import math


def lmtd(t_sat, t_in, t_out):
    """
    对数平均温差 LMTD (°C)
    公式：LMTD = (t_out - t_in) / ln[(t_sat - t_in)/(t_sat - t_out)]

    参数:
        t_sat: 饱和水温度 (°C)，必须> t_out
        t_in: 冷却水进水温度 (°C)，必须< t_out
        t_out: 冷却水出水温度 (°C)，必须> t_in 且 < t_sat
    返回:
        float: LMTD值 (°C)，保留4位小数
    """
    # 类型校验
    try:
        t_sat = float(t_sat)
        t_in = float(t_in)
        t_out = float(t_out)
    except (TypeError, ValueError):
        raise ValueError("所有温度输入必须为数字类型")

    # 温度顺序校验
    if not (t_sat > t_out > t_in):
        raise ValueError(f"温度顺序错误！必须满足 t_sat > t_out > t_in")
    
    if not (t_sat - t_out >= 2.8):
        raise ValueError(f"终端温差太小！必须满足 t_sat - t_out >= 2.8°C")

    dt1 = t_sat - t_in
    dt2 = t_sat - t_out

    if dt1 <= 0 or dt2 <= 0:
        raise ValueError(f"端温差必须为正！")

    # 核心计算
    if abs(dt1 - dt2) < 0.001:
        lmtd_value = dt1
    else:
        lmtd_value = (t_out - t_in) / math.log(dt1 / dt2)

    return round(lmtd_value, 4)


if __name__ == "__main__":
    print(lmtd(45.808, 32, 40))
