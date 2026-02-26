# HTAC凝汽器计算程序 - Android版

## 项目概述

工业级凝汽器（冷凝器）设计计算软件，基于Kivy框架开发的Android应用程序。

## 功能特性

### 核心计算功能
- **热负荷计算**: 根据蒸汽参数计算热负荷
- **冷却水计算**: 计算冷却水流量、温升、出口温度
- **传热系数**: 计算未修正/修正后的传热系数
- **LMTD计算**: 对数平均温差计算
- **换热面积**: 计算所需换热面积和设计面积
- **结构设计**: 计算管数、管长、管板直径、接管口径
- **水阻计算**: HEI标准冷却水阻力计算

### 计算模式
1. **温升模式**: 输入温升，自动计算水量
2. **水量模式**: 输入水量，自动计算温升

### 结构计算模式
1. **自动计算**: 输入流速，自动计算管数和管长
2. **手动输入**: 输入管数和管长，反算流速
3. **固定面积**: 输入设计面积和管数，计算管长和流速

## 技术架构

```
condenser_calc_app/
├── main.py                 # 主程序入口
├── buildozer.spec          # Buildozer配置文件
├── cond/                   # 核心计算模块
│   ├── __init__.py
│   ├── data_model.py       # 数据模型
│   ├── calculator.py       # 计算引擎
│   ├── steam_duty.py       # 蒸汽热负荷
│   ├── water_correction.py # 水温修正系数
│   ├── material_coefficient.py # 材料修正系数
│   ├── heat_transfer_coefficient.py # 传热系数
│   ├── lmtd.py             # 对数平均温差
│   ├── surface_area.py     # 换热面积
│   ├── fouling.py          # 污垢系数转换
│   ├── tube_structure.py   # 管结构计算
│   ├── tube_sheet.py       # 管板计算
│   └── pressure_drop.py    # 水阻计算
├── generate_keystore.sh    # 签名密钥生成脚本
├── build_apk.sh           # APK构建脚本
└── README.md              # 说明文档
```

## 构建说明

### 环境要求
- Python 3.8+
- Buildozer
- Android SDK/NDK
- JDK 8+

### 快速构建

1. **生成签名密钥**
   ```bash
   ./generate_keystore.sh
   ```

2. **构建APK**
   ```bash
   ./build_apk.sh
   ```

### 手动构建

```bash
# 安装依赖
pip install buildozer cython

# 生成签名密钥
keytool -genkey -v -keystore htac-release-key.keystore -alias htac -keyalg RSA -keysize 2048 -validity 10000

# 构建APK
buildozer android release
```

## 签名信息

- **密钥库**: htac-release-key.keystore
- **密钥别名**: htac
- **密钥库密码**: htac123456
- **密钥密码**: htac123456

## 界面设计

采用工业风格设计：
- 深蓝灰色背景 (#1E2327)
- 工业蓝主色调 (#328CD9)
- 橙色强调色 (#FFA500)
- 硬朗的线条和边框

## 版本历史

### v1.0.0
- 初始版本
- 实现核心计算功能
- 工业风格UI界面

## 许可证

版权所有 (C) 2024 HTAC
