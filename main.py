"""
凝汽器计算程序 - Android版
工业风格UI设计
"""
import os
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

from cond.data_model import InputData
from cond.calculator import CondenserCalculator
from cond.material_coefficient import get_material_list

# 工业风格颜色
COLORS = {
    'bg_dark': (0.12, 0.14, 0.16, 1),      # 深蓝灰背景
    'bg_panel': (0.18, 0.20, 0.23, 1),      # 面板背景
    'primary': (0.20, 0.55, 0.85, 1),       # 主色调（工业蓝）
    'accent': (1.0, 0.65, 0.0, 1),          # 强调色（橙色）
    'text': (0.9, 0.9, 0.9, 1),             # 主文字
    'text_secondary': (0.6, 0.6, 0.6, 1),   # 次要文字
    'border': (0.3, 0.35, 0.4, 1),          # 边框
    'input_bg': (0.25, 0.28, 0.32, 1),      # 输入框背景
    'success': (0.2, 0.8, 0.4, 1),          # 成功绿
    'warning': (1.0, 0.8, 0.2, 1),          # 警告黄
    'error': (0.9, 0.3, 0.3, 1),            # 错误红
}


class IndustrialLabel(Label):
    """工业风格标签"""
    def __init__(self, **kwargs):
        kwargs.setdefault('color', COLORS['text'])
        kwargs.setdefault('font_size', '14sp')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', '30dp')
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'center')
        super().__init__(**kwargs)
        self.bind(size=self.setter('text_size'))


class IndustrialInput(TextInput):
    """工业风格输入框"""
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', COLORS['input_bg'])
        kwargs.setdefault('foreground_color', COLORS['text'])
        kwargs.setdefault('cursor_color', COLORS['primary'])
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', '40dp')
        kwargs.setdefault('font_size', '14sp')
        kwargs.setdefault('multiline', False)
        kwargs.setdefault('padding', [10, 8])
        super().__init__(**kwargs)


class IndustrialButton(Button):
    """工业风格按钮"""
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', COLORS['primary'])
        kwargs.setdefault('color', (1, 1, 1, 1))
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', '45dp')
        kwargs.setdefault('font_size', '14sp')
        kwargs.setdefault('bold', True)
        super().__init__(**kwargs)


class IndustrialSpinner(Spinner):
    """工业风格下拉框"""
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', COLORS['input_bg'])
        kwargs.setdefault('color', COLORS['text'])
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', '40dp')
        kwargs.setdefault('font_size', '14sp')
        super().__init__(**kwargs)


class SectionHeader(BoxLayout):
    """分组标题"""
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = '35dp'
        self.padding = [0, 5]
        
        with self.canvas.before:
            Color(*COLORS['primary'][:3], 0.3)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        label = Label(
            text=title,
            color=COLORS['primary'],
            font_size='16sp',
            bold=True,
            halign='left',
            size_hint_x=1
        )
        label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        self.add_widget(label)
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class InputPanel(BoxLayout):
    """输入面板"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '5dp'
        self.padding = '10dp'
        
        # 创建滚动视图
        scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')
        self.content.bind(minimum_height=self.content.setter('height'))
        
        self._create_project_section()
        self._create_steam_section()
        self._create_tube_section()
        self._create_water_section()
        self._create_mode_section()
        self._create_structure_section()
        
        scroll.add_widget(self.content)
        self.add_widget(scroll)
    
    def _create_project_section(self):
        """项目信息"""
        self.content.add_widget(SectionHeader('项目信息'))
        
        grid = GridLayout(cols=2, spacing='5dp', size_hint_y=None, height='80dp')
        
        grid.add_widget(IndustrialLabel(text='项目名称:'))
        self.project_name = IndustrialInput(hint_text='输入项目名称')
        grid.add_widget(self.project_name)
        
        grid.add_widget(IndustrialLabel(text='工况名称:'))
        self.working_condition = IndustrialInput(hint_text='输入工况名称')
        grid.add_widget(self.working_condition)
        
        self.content.add_widget(grid)
    
    def _create_steam_section(self):
        """蒸汽参数"""
        self.content.add_widget(SectionHeader('蒸汽参数'))
        
        grid = GridLayout(cols=2, spacing='5dp', size_hint_y=None, height='120dp')
        
        grid.add_widget(IndustrialLabel(text='蒸汽压力 (MPa):'))
        self.steam_pressure = IndustrialInput(hint_text='0.01', input_filter='float')
        grid.add_widget(self.steam_pressure)
        
        grid.add_widget(IndustrialLabel(text='蒸汽流量 (kg/h):'))
        self.steam_mass_flow = IndustrialInput(hint_text='20', input_filter='float')
        grid.add_widget(self.steam_mass_flow)
        
        grid.add_widget(IndustrialLabel(text='蒸汽焓值 (kJ/kg):'))
        self.steam_enthalpy = IndustrialInput(hint_text='2345', input_filter='float')
        grid.add_widget(self.steam_enthalpy)
        
        self.content.add_widget(grid)
    
    def _create_tube_section(self):
        """换热管参数"""
        self.content.add_widget(SectionHeader('换热管参数'))
        
        grid = GridLayout(cols=2, spacing='5dp', size_hint_y=None, height='200dp')
        
        grid.add_widget(IndustrialLabel(text='换热管外径 (mm):'))
        self.tube_diameter = IndustrialInput(hint_text='20', input_filter='float')
        self.tube_diameter.bind(text=self._on_diameter_change)
        grid.add_widget(self.tube_diameter)
        
        grid.add_widget(IndustrialLabel(text='管壁厚度 (mm):'))
        self.tube_wall_thickness = IndustrialInput(hint_text='1', input_filter='float')
        grid.add_widget(self.tube_wall_thickness)
        
        grid.add_widget(IndustrialLabel(text='换热管间距 (mm):'))
        self.tube_pitch = IndustrialInput(hint_text='30', input_filter='float')
        grid.add_widget(self.tube_pitch)
        
        grid.add_widget(IndustrialLabel(text='换热管材质:'))
        self.material = IndustrialSpinner(
            text='SS TP 304',
            values=get_material_list()
        )
        grid.add_widget(self.material)
        
        grid.add_widget(IndustrialLabel(text='流程数:'))
        self.passes = IndustrialSpinner(
            text='2',
            values=['1', '2', '4']
        )
        grid.add_widget(self.passes)
        
        grid.add_widget(IndustrialLabel(text='冷却水管口数:'))
        self.nozzle_count = IndustrialSpinner(
            text='2',
            values=['1', '2']
        )
        grid.add_widget(self.nozzle_count)
        
        self.content.add_widget(grid)
    
    def _create_water_section(self):
        """冷却水参数"""
        self.content.add_widget(SectionHeader('冷却水参数'))
        
        grid = GridLayout(cols=2, spacing='5dp', size_hint_y=None, height='160dp')
        
        grid.add_widget(IndustrialLabel(text='进口温度 (°C):'))
        self.cooling_water_in_temp = IndustrialInput(hint_text='32', input_filter='float')
        grid.add_widget(self.cooling_water_in_temp)
        
        grid.add_widget(IndustrialLabel(text='比热容 (kJ/kg·°C):'))
        self.cp_water = IndustrialInput(hint_text='4.179', input_filter='float')
        grid.add_widget(self.cp_water)
        
        grid.add_widget(IndustrialLabel(text='密度 (kg/m³):'))
        self.rho_water = IndustrialInput(hint_text='997', input_filter='float')
        grid.add_widget(self.rho_water)
        
        grid.add_widget(IndustrialLabel(text='清洁系数:'))
        self.cleanliness_factor = IndustrialInput(hint_text='0.85', input_filter='float')
        grid.add_widget(self.cleanliness_factor)
        
        self.content.add_widget(grid)
    
    def _create_mode_section(self):
        """计算模式选择"""
        self.content.add_widget(SectionHeader('计算模式'))
        
        box = BoxLayout(size_hint_y=None, height='40dp', spacing='10dp')
        
        self.mode_temp_rise = ToggleButton(
            text='输入温升',
            group='calc_mode',
            state='down',
            background_color=COLORS['primary']
        )
        self.mode_water_flow = ToggleButton(
            text='输入水量',
            group='calc_mode',
            background_color=COLORS['input_bg']
        )
        
        self.mode_temp_rise.bind(on_press=self._on_mode_change)
        self.mode_water_flow.bind(on_press=self._on_mode_change)
        
        box.add_widget(self.mode_temp_rise)
        box.add_widget(self.mode_water_flow)
        
        self.content.add_widget(box)
        
        # 模式输入框
        self.mode_grid = GridLayout(cols=2, spacing='5dp', size_hint_y=None, height='40dp')
        
        self.label_temp_rise = IndustrialLabel(text='冷却水温升 (°C):')
        self.input_temp_rise = IndustrialInput(hint_text='8', input_filter='float')
        
        self.label_water_flow = IndustrialLabel(text='冷却水量 (m³/h):')
        self.input_water_flow = IndustrialInput(hint_text='1000', input_filter='float')
        self.input_water_flow.disabled = True
        self.input_water_flow.background_color = (0.15, 0.17, 0.19, 1)
        
        self.mode_grid.add_widget(self.label_temp_rise)
        self.mode_grid.add_widget(self.input_temp_rise)
        
        self.content.add_widget(self.mode_grid)
    
    def _create_structure_section(self):
        """结构计算模式"""
        self.content.add_widget(SectionHeader('结构计算模式'))
        
        box = BoxLayout(size_hint_y=None, height='40dp', spacing='5dp')
        
        self.structure_auto = ToggleButton(
            text='自动计算',
            group='structure_mode',
            state='down',
            background_color=COLORS['primary']
        )
        self.structure_manual = ToggleButton(
            text='手动输入',
            group='structure_mode',
            background_color=COLORS['input_bg']
        )
        self.structure_fixed = ToggleButton(
            text='固定面积',
            group='structure_mode',
            background_color=COLORS['input_bg']
        )
        
        self.structure_auto.bind(on_press=self._on_structure_change)
        self.structure_manual.bind(on_press=self._on_structure_change)
        self.structure_fixed.bind(on_press=self._on_structure_change)
        
        box.add_widget(self.structure_auto)
        box.add_widget(self.structure_manual)
        box.add_widget(self.structure_fixed)
        
        self.content.add_widget(box)
        
        # 结构参数输入
        self.structure_grid = GridLayout(cols=2, spacing='5dp', size_hint_y=None, height='80dp')
        
        self.label_velocity = IndustrialLabel(text='设计流速 (m/s):')
        self.input_velocity = IndustrialInput(hint_text='2.0', input_filter='float')
        
        self.label_tube_count = IndustrialLabel(text='换热管数量:')
        self.input_tube_count = IndustrialInput(hint_text='3600', input_filter='int')
        self.input_tube_count.disabled = True
        self.input_tube_count.background_color = (0.15, 0.17, 0.19, 1)
        
        self.label_tube_length = IndustrialLabel(text='换热管长度 (mm):')
        self.input_tube_length = IndustrialInput(hint_text='5000', input_filter='float')
        self.input_tube_length.disabled = True
        self.input_tube_length.background_color = (0.15, 0.17, 0.19, 1)
        
        self.label_design_surface = IndustrialLabel(text='设计面积 (m²):')
        self.input_design_surface = IndustrialInput(hint_text='1200', input_filter='float')
        self.input_design_surface.disabled = True
        self.input_design_surface.background_color = (0.15, 0.17, 0.19, 1)
        
        self.structure_grid.add_widget(self.label_velocity)
        self.structure_grid.add_widget(self.input_velocity)
        
        self.content.add_widget(self.structure_grid)
    
    def _on_diameter_change(self, instance, value):
        """管径变化时自动计算管间距"""
        try:
            diameter = float(value) if value else 0
            base_pitch = diameter * 1.25
            if base_pitch < 25:
                pitch = 25
            elif base_pitch < 30:
                pitch = 30
            elif base_pitch <= 32:
                pitch = 32
            elif base_pitch <= 38:
                pitch = 38
            else:
                pitch = base_pitch
            self.tube_pitch.text = str(round(pitch, 1))
        except:
            pass
    
    def _on_mode_change(self, instance):
        """计算模式切换"""
        if instance == self.mode_temp_rise:
            self.mode_grid.clear_widgets()
            self.mode_grid.add_widget(self.label_temp_rise)
            self.mode_grid.add_widget(self.input_temp_rise)
            self.input_temp_rise.disabled = False
            self.input_temp_rise.background_color = COLORS['input_bg']
            self.input_water_flow.disabled = True
            self.input_water_flow.background_color = (0.15, 0.17, 0.19, 1)
            self.mode_temp_rise.background_color = COLORS['primary']
            self.mode_water_flow.background_color = COLORS['input_bg']
        else:
            self.mode_grid.clear_widgets()
            self.mode_grid.add_widget(self.label_water_flow)
            self.mode_grid.add_widget(self.input_water_flow)
            self.input_water_flow.disabled = False
            self.input_water_flow.background_color = COLORS['input_bg']
            self.input_temp_rise.disabled = True
            self.input_temp_rise.background_color = (0.15, 0.17, 0.19, 1)
            self.mode_water_flow.background_color = COLORS['primary']
            self.mode_temp_rise.background_color = COLORS['input_bg']
    
    def _on_structure_change(self, instance):
        """结构模式切换"""
        self.structure_grid.clear_widgets()
        
        # 重置所有按钮颜色
        self.structure_auto.background_color = COLORS['input_bg']
        self.structure_manual.background_color = COLORS['input_bg']
        self.structure_fixed.background_color = COLORS['input_bg']
        instance.background_color = COLORS['primary']
        
        if instance == self.structure_auto:
            # 自动计算模式
            self.structure_grid.add_widget(self.label_velocity)
            self.structure_grid.add_widget(self.input_velocity)
            self.input_velocity.disabled = False
            self.input_velocity.background_color = COLORS['input_bg']
            self.input_tube_count.disabled = True
            self.input_tube_length.disabled = True
            self.input_design_surface.disabled = True
        elif instance == self.structure_manual:
            # 手动输入模式
            self.structure_grid.add_widget(self.label_tube_count)
            self.structure_grid.add_widget(self.input_tube_count)
            self.structure_grid.add_widget(self.label_tube_length)
            self.structure_grid.add_widget(self.input_tube_length)
            self.input_velocity.disabled = True
            self.input_tube_count.disabled = False
            self.input_tube_count.background_color = COLORS['input_bg']
            self.input_tube_length.disabled = False
            self.input_tube_length.background_color = COLORS['input_bg']
            self.input_design_surface.disabled = True
        else:
            # 固定面积模式
            self.structure_grid.add_widget(self.label_design_surface)
            self.structure_grid.add_widget(self.input_design_surface)
            self.structure_grid.add_widget(self.label_tube_count)
            self.structure_grid.add_widget(self.input_tube_count)
            self.input_velocity.disabled = True
            self.input_tube_count.disabled = False
            self.input_tube_count.background_color = COLORS['input_bg']
            self.input_tube_length.disabled = True
            self.input_design_surface.disabled = False
            self.input_design_surface.background_color = COLORS['input_bg']
    
    def get_input_data(self):
        """获取输入数据"""
        data = InputData()
        
        # 项目信息
        data.project_name = self.project_name.text or None
        data.working_condition = self.working_condition.text or None
        
        # 蒸汽参数
        data.steam_pressure = float(self.steam_pressure.text) if self.steam_pressure.text else None
        data.steam_mass_flow = float(self.steam_mass_flow.text) if self.steam_mass_flow.text else None
        data.steam_enthalpy = float(self.steam_enthalpy.text) if self.steam_enthalpy.text else None
        
        # 换热管参数
        data.tube_diameter = float(self.tube_diameter.text) if self.tube_diameter.text else None
        data.tube_wall_thickness = float(self.tube_wall_thickness.text) if self.tube_wall_thickness.text else None
        data.tube_pitch = float(self.tube_pitch.text) if self.tube_pitch.text else None
        data.material = self.material.text
        data.passes = int(self.passes.text)
        data.cooling_water_nozzle_count = int(self.nozzle_count.text)
        
        # 冷却水参数
        data.cooling_water_in_temp = float(self.cooling_water_in_temp.text) if self.cooling_water_in_temp.text else None
        data.cp_water = float(self.cp_water.text) if self.cp_water.text else None
        data.rho_water = float(self.rho_water.text) if self.rho_water.text else None
        data.cleanliness_factor = float(self.cleanliness_factor.text) if self.cleanliness_factor.text else None
        
        # 计算模式
        if self.mode_temp_rise.state == 'down':
            data.calculation_mode = 0
            data.cooling_water_temp_rise = float(self.input_temp_rise.text) if self.input_temp_rise.text else None
        else:
            data.calculation_mode = 1
            data.water_flow_input = float(self.input_water_flow.text) if self.input_water_flow.text else None
        
        # 结构模式
        if self.structure_auto.state == 'down':
            data.structure_mode = 0
            data.velocity = float(self.input_velocity.text) if self.input_velocity.text else None
        elif self.structure_manual.state == 'down':
            data.structure_mode = 1
            data.input_tube_count = int(self.input_tube_count.text) if self.input_tube_count.text else None
            data.input_tube_length = float(self.input_tube_length.text) if self.input_tube_length.text else None
        else:
            data.structure_mode = 2
            data.input_design_surface = float(self.input_design_surface.text) if self.input_design_surface.text else None
            data.input_tube_count = int(self.input_tube_count.text) if self.input_tube_count.text else None
        
        return data


class ResultPanel(BoxLayout):
    """结果面板"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '5dp'
        self.padding = '10dp'
        
        scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')
        self.content.bind(minimum_height=self.content.setter('height'))
        
        self._create_thermal_section()
        self._create_structure_section()
        self._create_hydraulic_section()
        
        scroll.add_widget(self.content)
        self.add_widget(scroll)
    
    def _create_result_row(self, label_text, value_text='-'):
        """创建结果行"""
        box = BoxLayout(size_hint_y=None, height='35dp', spacing='10dp')
        
        label = IndustrialLabel(
            text=label_text,
            size_hint_x=0.6
        )
        value = IndustrialLabel(
            text=value_text,
            color=COLORS['accent'],
            size_hint_x=0.4,
            bold=True
        )
        
        box.add_widget(label)
        box.add_widget(value)
        
        return box, value
    
    def _create_thermal_section(self):
        """热力计算结果"""
        self.content.add_widget(SectionHeader('热力计算结果'))
        
        self.saturation_temp, self.saturation_temp_value = self._create_result_row('饱和温度 (°C):')
        self.water_enthalpy, self.water_enthalpy_value = self._create_result_row('水焓值 (kJ/kg):')
        self.duty, self.duty_value = self._create_result_row('热负荷 (kW):')
        self.lmtd, self.lmtd_value = self._create_result_row('对数平均温差 (°C):')
        self.terminal_diff, self.terminal_diff_value = self._create_result_row('端差 (°C):')
        self.u_metric, self.u_metric_value = self._create_result_row('传热系数 (W/m²·°C):')
        self.surface_area, self.surface_area_value = self._create_result_row('计算换热面积 (m²):')
        self.design_surface, self.design_surface_value = self._create_result_row('设计换热面积 (m²):')
        
        self.content.add_widget(self.saturation_temp)
        self.content.add_widget(self.water_enthalpy)
        self.content.add_widget(self.duty)
        self.content.add_widget(self.lmtd)
        self.content.add_widget(self.terminal_diff)
        self.content.add_widget(self.u_metric)
        self.content.add_widget(self.surface_area)
        self.content.add_widget(self.design_surface)
    
    def _create_structure_section(self):
        """结构计算结果"""
        self.content.add_widget(SectionHeader('结构计算结果'))
        
        self.tube_count, self.tube_count_value = self._create_result_row('换热管数量:')
        self.tube_length, self.tube_length_value = self._create_result_row('换热管长度 (mm):')
        self.tube_sheet_dia, self.tube_sheet_dia_value = self._create_result_row('管板外径 (mm):')
        self.length_dia_ratio, self.length_dia_ratio_value = self._create_result_row('长径比:')
        
        self.content.add_widget(self.tube_count)
        self.content.add_widget(self.tube_length)
        self.content.add_widget(self.tube_sheet_dia)
        self.content.add_widget(self.length_dia_ratio)
    
    def _create_hydraulic_section(self):
        """水力计算结果"""
        self.content.add_widget(SectionHeader('水力计算结果'))
        
        self.water_flow_kg_s, self.water_flow_kg_s_value = self._create_result_row('冷却水量 (kg/s):')
        self.water_flow_m3_h, self.water_flow_m3_h_value = self._create_result_row('冷却水量 (m³/h):')
        self.outlet_temp, self.outlet_temp_value = self._create_result_row('冷却水出口温度 (°C):')
        self.pressure_drop, self.pressure_drop_value = self._create_result_row('冷却水阻 (MPa):')
        self.cw_nozzle, self.cw_nozzle_value = self._create_result_row('冷却水口内径 (mm):')
        self.cond_nozzle, self.cond_nozzle_value = self._create_result_row('凝结水口内径 (mm):')
        
        self.content.add_widget(self.water_flow_kg_s)
        self.content.add_widget(self.water_flow_m3_h)
        self.content.add_widget(self.outlet_temp)
        self.content.add_widget(self.pressure_drop)
        self.content.add_widget(self.cw_nozzle)
        self.content.add_widget(self.cond_nozzle)
    
    def update_results(self, data):
        """更新结果显示"""
        # 热力结果
        self.saturation_temp_value.text = f"{data.saturation_temp:.3f}" if data.saturation_temp else '-'
        self.water_enthalpy_value.text = f"{data.water_enthalpy:.3f}" if data.water_enthalpy else '-'
        self.duty_value.text = f"{data.DUTY:.3f}" if data.DUTY else '-'
        self.lmtd_value.text = f"{data.LMTD:.4f}" if data.LMTD else '-'
        self.terminal_diff_value.text = f"{data.terminal_temp_diff:.3f}" if data.terminal_temp_diff else '-'
        self.u_metric_value.text = f"{data.u_metric:.2f}" if data.u_metric else '-'
        self.surface_area_value.text = f"{data.surface_area:.2f}" if data.surface_area else '-'
        self.design_surface_value.text = f"{data.design_surface_area:.0f}" if data.design_surface_area else '-'
        
        # 结构结果
        self.tube_count_value.text = str(data.tube_count) if data.tube_count else '-'
        self.tube_length_value.text = f"{data.tube_length:.0f}" if data.tube_length else '-'
        self.tube_sheet_dia_value.text = f"{data.tube_sheet_diameter:.0f}" if data.tube_sheet_diameter else '-'
        self.length_dia_ratio_value.text = f"{data.tube_length_diameter_ratio:.2f}" if data.tube_length_diameter_ratio else '-'
        
        # 长径比颜色判断
        if data.tube_length_diameter_ratio:
            if data.tube_length_diameter_ratio < 2 or data.tube_length_diameter_ratio > 3:
                self.length_dia_ratio_value.color = COLORS['error']
            else:
                self.length_dia_ratio_value.color = COLORS['success']
        
        # 水力结果
        self.water_flow_kg_s_value.text = f"{data.water_flow_kg_s:.3f}" if data.water_flow_kg_s else '-'
        self.water_flow_m3_h_value.text = f"{data.water_flow_m3_h:.2f}" if data.water_flow_m3_h else '-'
        self.outlet_temp_value.text = f"{data.cooling_water_out_temp:.3f}" if data.cooling_water_out_temp else '-'
        self.pressure_drop_value.text = f"{data.total_pressure_drop:.6f}" if data.total_pressure_drop else '-'
        self.cw_nozzle_value.text = str(data.cooling_water_nozzle_diameter) if data.cooling_water_nozzle_diameter else '-'
        self.cond_nozzle_value.text = str(data.condensate_outlet_inner_diameter) if data.condensate_outlet_inner_diameter else '-'


class CondenserCalcApp(App):
    """主应用"""
    def build(self):
        Window.clearcolor = COLORS['bg_dark']
        
        root = BoxLayout(orientation='vertical', padding='5dp', spacing='5dp')
        
        # 标题栏
        title_bar = BoxLayout(size_hint_y=None, height='50dp', padding='5dp')
        with title_bar.canvas.before:
            Color(*COLORS['primary'][:3], 0.2)
            self.title_rect = Rectangle(pos=title_bar.pos, size=title_bar.size)
        title_bar.bind(pos=self._update_title_rect, size=self._update_title_rect)
        
        title_label = Label(
            text='◤◤HTAC◢◢ 凝汽器计算程序',
            font_size='18sp',
            bold=True,
            color=COLORS['primary']
        )
        title_bar.add_widget(title_label)
        root.add_widget(title_bar)
        
        # 标签页
        tabs = TabbedPanel(
            do_default_tab=False,
            tab_height='40dp',
            background_color=COLORS['bg_panel']
        )
        
        # 输入标签页
        input_tab = TabbedPanelHeader(text='参数输入')
        self.input_panel = InputPanel()
        input_tab.content = self.input_panel
        tabs.add_widget(input_tab)
        
        # 结果标签页
        result_tab = TabbedPanelHeader(text='计算结果')
        self.result_panel = ResultPanel()
        result_tab.content = self.result_panel
        tabs.add_widget(result_tab)
        
        root.add_widget(tabs)
        
        # 计算按钮
        calc_btn = IndustrialButton(
            text='执行计算',
            size_hint_y=None,
            height='50dp'
        )
        calc_btn.bind(on_press=self.on_calculate)
        root.add_widget(calc_btn)
        
        return root
    
    def _update_title_rect(self, instance, value):
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size
    
    def on_calculate(self, instance):
        """执行计算"""
        try:
            # 获取输入数据
            data = self.input_panel.get_input_data()
            
            # 验证必要参数
            errors = []
            if data.steam_pressure is None:
                errors.append('蒸汽压力')
            if data.steam_mass_flow is None:
                errors.append('蒸汽流量')
            if data.steam_enthalpy is None:
                errors.append('蒸汽焓值')
            if data.tube_diameter is None:
                errors.append('换热管外径')
            if data.tube_wall_thickness is None:
                errors.append('管壁厚度')
            if data.cooling_water_in_temp is None:
                errors.append('冷却水进口温度')
            
            if errors:
                self.show_error(f"请填写以下参数:\n{', '.join(errors)}")
                return
            
            # 执行计算
            calculator = CondenserCalculator(data)
            result_data = calculator.calculate_all()
            
            # 更新结果
            self.result_panel.update_results(result_data)
            
            # 显示成功提示
            self.show_success('计算完成！')
            
        except ValueError as e:
            self.show_error(f'输入错误: {str(e)}')
        except Exception as e:
            self.show_error(f'计算错误: {str(e)}')
    
    def show_error(self, message):
        """显示错误弹窗"""
        popup = Popup(
            title='错误',
            content=Label(text=message, color=COLORS['error']),
            size_hint=(0.8, 0.4),
            background_color=COLORS['bg_panel']
        )
        popup.open()
    
    def show_success(self, message):
        """显示成功弹窗"""
        popup = Popup(
            title='成功',
            content=Label(text=message, color=COLORS['success']),
            size_hint=(0.6, 0.3),
            background_color=COLORS['bg_panel']
        )
        popup.open()


if __name__ == '__main__':
    CondenserCalcApp().run()
