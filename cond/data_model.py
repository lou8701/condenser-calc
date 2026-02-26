"""
数据模型类 - 用于存储输入输出参数
"""


class InputData:
    """冷凝器计算输入参数容器"""

    def __init__(self):
        # 项目信息
        self.project_name = None
        self.working_condition = None

        # 输入参数
        self.tube_diameter = None
        self.steam_pressure = None
        self.steam_mass_flow = None
        self.steam_enthalpy = None
        self.tube_wall_thickness = None
        self.tube_pitch = None
        self.material = None
        self.cooling_water_in_temp = None
        self.cooling_water_temp_rise = None
        self.cp_water = None
        self.rho_water = None
        self.velocity = None
        self.cleanliness_factor = None
        self.fouling_factor = None
        self.passes = None
        self.cooling_water_nozzle_count = None

        # 计算结果
        self.saturation_temp = None
        self.water_enthalpy = None
        self.DUTY = None
        self.LMTD = None
        self.u_metric = None
        self.u_btu = None
        self.cooling_water_out_temp = None
        self.water_correction_factor = None
        self.material_coefficient = None
        self.clean_factor_corrected = None
        self.water_flow_kg_s = None
        self.water_flow_m3_h = None
        self.surface_area = None
        self.design_surface_area = None
        self.tube_length = None
        self.tube_count = None
        self.tube_sheet_diameter = None
        self.condensate_outlet_inner_diameter = None
        self.cooling_water_nozzle_diameter = None
        self.tube_length_diameter_ratio = None
        self.total_pressure_drop = None
        self.terminal_temp_diff = None

        # 计算模式
        self.calculation_mode = 0  # 0=输入温升, 1=输入水量
        self.water_flow_input = None

        # 结构计算模式
        self.structure_mode = 0  # 0=自动, 1=手动, 2=固定面积
        self.input_tube_count = None
        self.input_tube_length = None
        self.input_design_surface = None

    def to_dict(self):
        """转换为字典"""
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data_dict):
        """从字典创建"""
        obj = cls()
        for k, v in data_dict.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj


if __name__ == "__main__":
    data = InputData()
    data.steam_pressure = 0.01
    print(data.to_dict())
