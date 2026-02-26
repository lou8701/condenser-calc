"""
冷凝器计算引擎
"""
import math
from .data_model import InputData
from .steam_duty import get_steam_heat_load
from .water_correction import water_correction_factor
from .material_coefficient import material_coeff
from .heat_transfer_coefficient import uncorrected_u
from .lmtd import lmtd
from .surface_area import heat_transfer_area
from .fouling import fouling_to_clean
from .tube_structure import (
    calc_tube_count_from_flow, 
    calc_tube_length_from_area,
    calculate_pipe_inner_diameter,
    calc_tube_velocity
)
from .tube_sheet import calculate_tube_sheet_diameter
from .pressure_drop import calculate_hei_water_resistance


class CondenserCalculator:
    """纯计算引擎"""

    def __init__(self, data):
        self.data = data

    def calculate_all(self):
        """执行全部计算"""
        self._calc_steam_duty()
        self._calc_cooling_water()
        self._calc_material_coefficient()
        self._calc_water_correction_factor()
        self._calc_uncorrected_u()
        self._calc_lmtd()
        self._calc_fouling2clean()
        self._calc_surface_area()

        # 根据结构计算模式选择路径
        if self.data.structure_mode == 0:
            self._cal_design_surface_area()
            self._calc_tube_count()
            self._calc_tube_length()
        elif self.data.structure_mode == 1:
            self._calc_from_given_structure()
        else:
            self._calc_from_fixed_area()

        self._calc_tube_sheet_diameter()
        self._calc_pipe_diameter()
        self._calc_total_pressure_drop()
        self._calc_terminal_temp_diff()
        return self.data

    def _calc_steam_duty(self):
        """计算蒸汽热负荷"""
        if None in (self.data.steam_pressure, self.data.steam_enthalpy, self.data.steam_mass_flow):
            return
        sat_temp, water_enth, duty = get_steam_heat_load(
            self.data.steam_pressure,
            self.data.steam_enthalpy,
            self.data.steam_mass_flow / 3600  # kg/h -> kg/s
        )
        self.data.saturation_temp = sat_temp
        self.data.water_enthalpy = water_enth
        self.data.DUTY = duty

    def _calc_cooling_water(self):
        """计算冷却水参数"""
        cp_water = self.data.cp_water
        rho_water = self.data.rho_water

        if self.data.calculation_mode == 0:
            # 模式A：输入温升，计算水量
            temp_rise = self.data.cooling_water_temp_rise
            mass_flow_kg_s = self.data.DUTY / (cp_water * temp_rise)
            water_flow_m3_h = (mass_flow_kg_s / rho_water) * 3600
        else:
            # 模式B：输入水量，计算温升
            water_flow_m3_h = self.data.water_flow_input
            mass_flow_kg_s = (water_flow_m3_h * rho_water) / 3600
            temp_rise = self.data.DUTY / (mass_flow_kg_s * cp_water)

        # 计算出口温度
        cooling_water_out_temp = self.data.cooling_water_in_temp + temp_rise

        # 保存结果
        self.data.water_flow_kg_s = mass_flow_kg_s
        self.data.water_flow_m3_h = water_flow_m3_h
        self.data.cooling_water_temp_rise = temp_rise
        self.data.cooling_water_out_temp = cooling_water_out_temp

    def _calc_material_coefficient(self):
        """计算材料修正系数"""
        if None in (self.data.material, self.data.tube_wall_thickness):
            return
        self.data.material_coefficient = material_coeff(
            self.data.material,
            self.data.tube_wall_thickness / 25.4  # mm -> inch
        )

    def _calc_water_correction_factor(self):
        """计算水温修正系数"""
        if self.data.cooling_water_in_temp is None:
            return
        self.data.water_correction_factor = water_correction_factor(
            self.data.cooling_water_in_temp
        )

    def _calc_uncorrected_u(self):
        """计算未修正传热系数"""
        if None in (self.data.tube_diameter, self.data.velocity):
            return
        u_btu = uncorrected_u(self.data.tube_diameter, self.data.velocity)
        u_metric = u_btu * 5.678
        self.data.u_btu = u_btu
        self.data.u_metric = u_metric

    def _calc_lmtd(self):
        """计算对数平均温差"""
        if None in (self.data.saturation_temp, self.data.cooling_water_in_temp, self.data.cooling_water_temp_rise):
            return
        t_sat = self.data.saturation_temp
        t_in = self.data.cooling_water_in_temp
        t_out = t_in + self.data.cooling_water_temp_rise
        lmtd_value = lmtd(t_sat, t_in, t_out)
        self.data.cooling_water_out_temp = t_out
        self.data.LMTD = lmtd_value

    def _calc_fouling2clean(self):
        """计算修正清洁系数"""
        cf_input = self.data.cleanliness_factor
        f_input = self.data.fouling_factor
        corrected_u = self.data.u_metric * self.data.water_correction_factor * self.data.material_coefficient
        
        if f_input is not None and f_input > 0:
            self.data.clean_factor_corrected = fouling_to_clean(
                f_input,
                self.data.tube_diameter,
                self.data.tube_wall_thickness,
                corrected_u
            )
        elif cf_input is not None:
            self.data.clean_factor_corrected = cf_input

    def _calc_surface_area(self):
        """计算换热面积"""
        required_params = [
            self.data.DUTY, self.data.LMTD, self.data.u_metric,
            self.data.water_correction_factor, self.data.material_coefficient,
            self.data.clean_factor_corrected
        ]
        if None in required_params:
            return
        self.data.surface_area = heat_transfer_area(
            self.data.DUTY,
            self.data.LMTD,
            self.data.u_metric,
            self.data.water_correction_factor,
            self.data.material_coefficient,
            self.data.clean_factor_corrected
        )

    def _cal_design_surface_area(self):
        """计算设计换热面积"""
        if self.data.design_surface_area is not None:
            return
        if self.data.surface_area is None:
            self.data.design_surface_area = None
            return

        if self.data.fouling_factor is not None:
            self.data.design_surface_area = math.ceil(self.data.surface_area / 50) * 50
        else:
            surface_area_with_5pct = self.data.surface_area * (1 + 0.05)
            self.data.design_surface_area = math.ceil(surface_area_with_5pct / 50) * 50

    def _calc_tube_count(self):
        """计算换热管数量"""
        if None in (self.data.water_flow_m3_h, self.data.velocity, self.data.tube_diameter,
                    self.data.tube_wall_thickness, self.data.passes):
            return
        count = calc_tube_count_from_flow(
            self.data.water_flow_m3_h,
            self.data.velocity,
            self.data.tube_diameter,
            self.data.tube_wall_thickness,
            int(self.data.passes)
        )
        self.data.tube_count = count

    def _calc_tube_length(self):
        """计算换热管长度"""
        target_surface_area = self.data.design_surface_area if self.data.design_surface_area is not None else self.data.surface_area
        if None in (target_surface_area, self.data.tube_count, self.data.tube_diameter):
            return
        self.data.tube_length = calc_tube_length_from_area(
            target_surface_area,
            self.data.tube_count,
            self.data.tube_diameter
        )

    def _calc_from_given_structure(self):
        """模式1：根据给定的换热管数量和长度，反算流速和设计面积"""
        if self.data.input_tube_count is not None:
            self.data.tube_count = self.data.input_tube_count
        if self.data.input_tube_length is not None:
            self.data.tube_length = self.data.input_tube_length

        # 计算设计换热面积
        if all(v is not None for v in [self.data.tube_count, self.data.tube_length, self.data.tube_diameter]):
            tube_length_m = self.data.tube_length / 1000  # mm -> m
            self.data.design_surface_area = math.pi * (self.data.tube_diameter / 1000) * tube_length_m * self.data.tube_count
        
        # 反算流速
        self._calc_velocity_from_tube_count()

    def _calc_from_fixed_area(self):
        """模式2：固定设计面积 + 输入管数，计算管长和流速"""
        if self.data.input_design_surface is not None:
            self.data.design_surface_area = self.data.input_design_surface
        if self.data.input_tube_count is not None:
            self.data.tube_count = self.data.input_tube_count

        # 计算管长
        if all(v is not None for v in [self.data.design_surface_area, self.data.tube_diameter, self.data.tube_count]):
            tube_length_m = self.data.design_surface_area / (math.pi * (self.data.tube_diameter / 1000) * self.data.tube_count)
            self.data.tube_length = tube_length_m * 1000  # m -> mm

        # 反算流速
        self._calc_velocity_from_tube_count()

    def _calc_velocity_from_tube_count(self):
        """根据管数反算流速"""
        if all(v is not None for v in [self.data.water_flow_m3_h, self.data.tube_count,
                                       self.data.tube_diameter, self.data.tube_wall_thickness,
                                       self.data.passes]):
            di_m = (self.data.tube_diameter - 2 * self.data.tube_wall_thickness) / 1000
            area_per_tube = math.pi * (di_m / 2) ** 2
            flow_m3_s = self.data.water_flow_m3_h / 3600
            calculated_velocity = (flow_m3_s * self.data.passes) / (area_per_tube * self.data.tube_count)
            self.data.velocity = round(calculated_velocity, 3)

    def _calc_tube_sheet_diameter(self):
        """计算管板外径"""
        if None in (self.data.tube_count, self.data.passes, self.data.tube_pitch, self.data.tube_diameter):
            return
        try:
            self.data.tube_sheet_diameter = math.ceil(calculate_tube_sheet_diameter(
                self.data.tube_diameter,
                int(self.data.tube_count),
                int(self.data.passes),
                self.data.tube_pitch
            ))
        except Exception as e:
            print(f"计算管板外径失败：{e}")
            self.data.tube_sheet_diameter = None

    def _calc_pipe_diameter(self):
        """计算接管直径"""
        # 凝结水口
        a = calculate_pipe_inner_diameter(self.data.steam_mass_flow / 3600, 0.5, 1)
        self.data.condensate_outlet_inner_diameter = a
        
        # 冷却水口
        b = calculate_pipe_inner_diameter(
            self.data.water_flow_kg_s / self.data.cooling_water_nozzle_count,
            2, 2.5, self.data.rho_water
        )
        self.data.cooling_water_nozzle_diameter = b
        
        # 长径比
        if self.data.tube_length and self.data.tube_sheet_diameter:
            self.data.tube_length_diameter_ratio = round(self.data.tube_length / self.data.tube_sheet_diameter, 2)

    def _calc_total_pressure_drop(self):
        """计算总水阻"""
        temp_c = (self.data.cooling_water_in_temp + self.data.cooling_water_out_temp) / 2
        di_mm = self.data.tube_diameter - 2 * self.data.tube_wall_thickness
        self.data.total_pressure_drop = 1.2 * 0.001 * calculate_hei_water_resistance(
            di_mm, self.data.velocity, self.data.tube_length, self.data.passes, temp_c
        )

    def _calc_terminal_temp_diff(self):
        """计算端差"""
        if self.data.saturation_temp is None or self.data.cooling_water_out_temp is None:
            return
        self.data.terminal_temp_diff = self.data.saturation_temp - self.data.cooling_water_out_temp
