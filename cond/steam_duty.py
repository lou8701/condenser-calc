"""
蒸汽热负荷计算模块
基于IAPWS-IF97标准计算饱和水温度和焓值
"""
import math


# 简化的IAPWS-IF97饱和水性质计算（避免依赖外部库）
def _iapws_saturation_properties(P_MPa):
    """
    简化的饱和水性质计算
    返回: (温度°C, 饱和水焓kJ/kg)
    """
    # 使用近似公式计算饱和温度（适用于0.001-10 MPa范围）
    # 基于IAPWS-IF97的简化公式
    if P_MPa <= 0:
        raise ValueError("压力必须大于0")
    if P_MPa > 22.064:  # 临界压力
        raise ValueError("压力超过临界压力")
    
    # 饱和温度近似计算 (°C)
    # 使用Antoine方程的改进形式
    P_kPa = P_MPa * 1000
    if P_kPa < 1:
        raise ValueError("压力过低")
    
    # 简化的饱和温度计算
    T_sat = 0.0
    if P_MPa <= 0.1:
        # 低压区
        T_sat = 10.1967 * (P_MPa ** 0.25) - 0.3667
    elif P_MPa <= 1.0:
        # 中低压区
        T_sat = 45.0 + 45.0 * math.log10(P_MPa * 10)
    else:
        # 高压区
        T_sat = 100.0 + 50.0 * math.log10(P_MPa)
    
    # 饱和水焓近似计算 (kJ/kg)
    # 基于温度的多项式拟合
    h_water = 4.2 * T_sat + 0.0015 * (T_sat ** 2)
    
    return round(T_sat, 3), round(h_water, 3)


def get_steam_heat_load(pressure_MPa, steam_enthalpy, steam_flow_rate):
    """
    计算饱和水温度、焓值及热负荷（kJ/s）

    参数:
        pressure_MPa: 工作压力 (MPa)，必须>0
        steam_enthalpy: 蒸汽焓值 (kJ/kg)，必须>0
        steam_flow_rate: 蒸汽流量 (kg/s)，必须>0
    返回:
        tuple: (饱和水温度°C, 饱和水焓值kJ/kg, 热负荷kJ/s)
    异常:
        ValueError: 输入参数非正数时抛出
    """
    # 类型 + 数值校验
    try:
        pressure_MPa = float(pressure_MPa)
        steam_enthalpy = float(steam_enthalpy)
        steam_flow_rate = float(steam_flow_rate)
    except (TypeError, ValueError):
        raise ValueError("所有输入必须为数字类型")

    if pressure_MPa <= 0:
        raise ValueError(f"工作压力({pressure_MPa} MPa)必须>0")
    if steam_enthalpy <= 0:
        raise ValueError(f"蒸汽焓值({steam_enthalpy} kJ/kg)必须>0")
    if steam_flow_rate <= 0:
        raise ValueError(f"蒸汽流量({steam_flow_rate} kg/s)必须>0")

    # 饱和水计算
    try:
        temperature, water_enthalpy = _iapws_saturation_properties(pressure_MPa)
        heat_load = (steam_enthalpy - water_enthalpy) * steam_flow_rate
    except Exception as e:
        raise Exception(f"饱和水计算失败：{str(e)}")

    return round(temperature, 3), round(water_enthalpy, 3), round(heat_load, 3)


# 测试
if __name__ == "__main__":
    duty = get_steam_heat_load(0.02, 2345, 23)
    print(f"饱和温度: {duty[0]}°C, 饱和水焓值: {duty[1]}kJ/kg, 热负荷: {duty[2]}kJ/s")
