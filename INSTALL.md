# HTAC凝汽器计算程序 - 安装指南

## 方法一：直接运行Python源码（推荐）

### 在Android上运行

#### 使用 Pydroid 3（推荐）
1. 从Google Play下载并安装 **Pydroid 3**
2. 打开Pydroid 3，点击左上角菜单 → **Pip**
3. 安装依赖库：
   ```
   kivy
   ```
4. 将 `condenser_calc_app` 文件夹复制到手机存储
5. 在Pydroid 3中打开 `android_run.py`
6. 点击运行按钮（▶️）

#### 使用 QPython
1. 从Google Play下载并安装 **QPython 3L**
2. 将 `condenser_calc_app` 文件夹复制到 `/sdcard/qpython/projects3/`
3. 打开QPython，选择项目运行

### 在Windows/Mac/Linux上运行

1. 安装Python 3.8+
2. 安装依赖：
   ```bash
   pip install kivy
   ```
3. 运行程序：
   ```bash
   python android_run.py
   ```

## 方法二：构建APK安装包

### 环境准备

1. **安装Python 3.8+**
2. **安装Java JDK 8+**
3. **安装Android SDK/NDK**（可选，buildozer会自动下载）

### 安装Buildozer

```bash
pip install buildozer cython
```

### 构建步骤

1. **进入项目目录**
   ```bash
   cd condenser_calc_app
   ```

2. **生成签名密钥**（首次需要）
   ```bash
   # Linux/Mac
   ./generate_keystore.sh
   
   # Windows
   keytool -genkey -v -keystore htac-release-key.keystore -alias htac -keyalg RSA -keysize 2048 -validity 10000
   ```

3. **构建APK**
   ```bash
   # 使用脚本
   ./build_apk.sh
   
   # 或手动构建
   buildozer android release
   ```

4. **获取APK**
   - 构建完成后，APK文件位于 `./bin/` 目录
   - 文件名格式：`condensercalc-1.0.0-arm64-v8a_armeabi-v7a-release.apk`

### 签名信息

- **密钥库**: htac-release-key.keystore
- **密钥别名**: htac
- **密钥库密码**: htac123456
- **密钥密码**: htac123456

## 方法三：使用在线构建服务

### 使用Buildozer Cloud（推荐）

1. 访问 https://buildozer.io/
2. 上传项目源码压缩包
3. 等待构建完成
4. 下载生成的APK

### 使用GitHub Actions

1. 将代码推送到GitHub仓库
2. 添加 `.github/workflows/build.yml` 工作流文件
3. GitHub Actions会自动构建APK
4. 从Actions页面下载构建产物

## 常见问题

### Q: 安装后无法运行？
A: 请确保：
- Android版本 5.0+
- 已授予存储权限
- 从可信来源安装APK

### Q: 计算结果不准确？
A: 请检查：
- 输入参数单位是否正确
- 温度范围是否在有效区间内
- 管径是否在支持范围内（15.875-50.8mm）

### Q: 如何更新软件？
A: 直接安装新版本APK即可，旧版本会被覆盖。

## 技术支持

如有问题，请检查：
1. README.md 中的技术文档
2. 代码中的注释说明
3. 原始Python版本的文档
