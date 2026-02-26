# HTAC凝汽器计算 - 快速开始指南

## 获取APK的三种方式

### 方式一：GitHub Actions自动构建（推荐，最简单）

**预计时间：25分钟**

#### 步骤1：创建GitHub账号
- 访问 https://github.com/signup
- 注册账号（免费）

#### 步骤2：创建仓库
1. 登录GitHub
2. 点击右上角 **+** → **New repository**
3. 输入仓库名：`condenser-calc`
4. 选择 **Public**
5. 点击 **Create repository**

#### 步骤3：上传代码
```bash
# 下载并解压源码包
unzip condenser_calc_app_complete.zip
cd condenser_calc_app

# 初始化git
git init
git add .
git commit -m "Initial commit"

# 推送到GitHub（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/condenser-calc.git
git push -u origin main
```

#### 步骤4：等待自动构建
1. 打开仓库页面
2. 点击 **Actions** 标签
3. 等待构建完成（约20分钟）
4. 完成后点击 **Releases** 下载APK

---

### 方式二：本地构建（需要Linux环境）

**预计时间：2-3小时（首次）**

#### 环境要求
- Ubuntu 20.04+ / Debian 10+
- Python 3.8+
- Java JDK 11+
- 至少 10GB 磁盘空间

#### 安装步骤
```bash
# 1. 安装系统依赖
sudo apt-get update
sudo apt-get install -y \
    git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev automake libltdl-dev

# 2. 安装Python依赖
pip install buildozer cython

# 3. 进入项目目录
cd condenser_calc_app

# 4. 生成签名密钥（已包含在源码包中）
# 如需重新生成：
# ./generate_keystore.sh

# 5. 构建APK
./build_apk.sh

# 6. 获取APK
ls bin/*.apk
```

---

### 方式三：Android直接运行（无需构建）

**预计时间：5分钟**

#### 步骤1：安装Pydroid 3
1. 在Google Play搜索 **Pydroid 3**
2. 下载并安装

#### 步骤2：安装Kivy
1. 打开Pydroid 3
2. 点击左上角菜单 → **Pip**
3. 输入：`kivy`
4. 点击 **INSTALL**

#### 步骤3：运行程序
1. 将 `condenser_calc_app` 文件夹复制到手机
2. 在Pydroid 3中打开 `android_run.py`
3. 点击运行按钮（▶️）

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `main.py` | 主程序入口 |
| `android_run.py` | Android直接运行版 |
| `buildozer.spec` | Buildozer配置文件 |
| `build_apk.sh` | APK构建脚本 |
| `generate_keystore.sh` | 签名密钥生成脚本 |
| `htac-release-key.keystore` | 签名密钥（已生成） |
| `cond/` | 核心计算模块 |
| `.github/workflows/` | GitHub Actions配置 |

---

## 签名信息

```
密钥库: htac-release-key.keystore
密钥别名: htac
密钥库密码: htac123456
密钥密码: htac123456
有效期: 10000天
```

---

## 常见问题

### Q: GitHub Actions构建失败？

**检查清单：**
- [ ] 代码是否正确上传
- [ ] buildozer.spec 是否在根目录
- [ ] 是否推送到了 main/master 分支

**查看日志：**
1. 打开仓库 → Actions
2. 点击失败的 workflow
3. 查看详细错误信息

### Q: 本地构建太慢？

**优化建议：**
- 只构建一个架构：`android.archs = arm64-v8a`
- 使用SSD硬盘
- 确保网络连接稳定

### Q: APK安装失败？

**解决方案：**
1. 允许安装未知来源应用
   - 设置 → 安全 → 未知来源 → 允许
2. 检查Android版本（需要5.0+）
3. 卸载旧版本后重新安装

---

## 技术支持

如有问题，请提供：
1. 使用的构建方式
2. 错误日志截图
3. 系统环境信息
