"""
换热管材料修正系数模块
"""

# 壁厚序列（英寸）
_THICKNESS = [0.020, 0.022, 0.025, 0.028, 0.035,
              0.049, 0.065, 0.083, 0.109]

# 材料 -> 修正系数序列
_COEFF = {
    "Cu Fe 194": [1.042, 1.041, 1.039, 1.038, 1.034, 1.028, 1.020, 1.010, 0.997],
    "Arsenical Cu": [1.038, 1.037, 1.035, 1.033, 1.029, 1.020, 1.010, 0.997, 0.979],
    "Admiralty": [1.029, 1.027, 1.024, 1.021, 1.013, 0.998, 0.981, 0.961, 0.932],
    "Al Brass": [1.027, 1.025, 1.021, 1.018, 1.010, 0.993, 0.974, 0.952, 0.921],
    "Al Bronze": [1.021, 1.018, 1.014, 1.009, 0.999, 0.979, 0.956, 0.930, 0.892],
    "Carbon Steel": [1.002, 0.998, 0.990, 0.983, 0.967, 0.936, 0.901, 0.863, 0.810],
    "Cu Ni 90-10": [1.000, 0.995, 0.987, 0.980, 0.963, 0.930, 0.893, 0.854, 0.800],
    "Cu Ni 70-30": [0.974, 0.967, 0.957, 0.946, 0.922, 0.876, 0.828, 0.777, 0.710],
    "SS(UNS S43035)": [0.959, 0.951, 0.938, 0.926, 0.898, 0.846, 0.792, 0.736, 0.664],
    "Titanium Grades 1 &2": [0.951, 0.942, 0.928, 0.915, 0.885, 0.830, 0.772, 0.714, 0.640],
    "SS (UNS S44660)": [0.928, 0.917, 0.901, 0.886, 0.851, 0.787, 0.723, 0.659, 0.581],
    "SS (UNS S44735)": [0.926, 0.915, 0.899, 0.883, 0.847, 0.783, 0.718, 0.654, 0.576],
    "SS TP 304": [0.910, 0.897, 0.879, 0.862, 0.823, 0.754, 0.685, 0.619, 0.539],
    "SS TP 316/317": [0.904, 0.891, 0.872, 0.854, 0.815, 0.744, 0.674, 0.607, 0.527],
    "SS (UNS N08367)": [0.879, 0.864, 0.843, 0.823, 0.779, 0.702, 0.628, 0.558, 0.477],
    "ATI 2003 (UNS S32003)": [0.927, 0.916, 0.900, 0.884, 0.849, 0.785, 0.721, 0.657, 0.578],
    "2205 (UNS S31803, S32205)": [0.907, 0.894, 0.876, 0.858, 0.819, 0.749, 0.680, 0.613, 0.533],
    "2507 (UNS S32750)": [0.911, 0.899, 0.881, 0.864, 0.825, 0.756, 0.688, 0.622, 0.542],
}

_VALID_MATERIALS = list(_COEFF.keys())
_MIN_THICK = _THICKNESS[0]
_MAX_THICK = _THICKNESS[-1]


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


def material_coeff(material, thickness_in):
    """
    换热管材料修正系数（线性插值，保留4位小数）

    参数:
        material: 材料名称
        thickness_in: 壁厚 (英寸)，范围 [0.020, 0.109]
    返回:
        float: 材料修正系数（4位小数）
    """
    # 类型校验
    try:
        thickness_in = float(thickness_in)
    except (TypeError, ValueError):
        raise TypeError(f"壁厚必须为数字类型")

    # 材料名称标准化 + 校验
    material_clean = material.strip()
    key = None
    for k in _VALID_MATERIALS:
        if k.lower() == material_clean.lower():
            key = k
            break
    
    if key is None:
        raise ValueError(f"未知材料：{material}")

    # 壁厚范围校验
    if not (_MIN_THICK <= thickness_in <= _MAX_THICK):
        raise ValueError(
            f"壁厚超出范围！允许范围：[{_MIN_THICK}, {_MAX_THICK}] 英寸"
        )

    # 线性插值
    coeff = _linear_interp(thickness_in, _THICKNESS, _COEFF[key])
    return round(coeff, 4)


def get_material_list():
    """获取支持的材料列表"""
    return _VALID_MATERIALS.copy()


if __name__ == "__main__":
    print(material_coeff("SS TP 304", 0.049))
    print(get_material_list())
