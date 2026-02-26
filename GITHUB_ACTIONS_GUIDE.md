# GitHub Actions 自动构建APK - 完整指南

## 概述

GitHub Actions 是 GitHub 提供的持续集成/持续部署(CI/CD)服务，可以自动构建、测试和部署代码。

本指南将详细介绍如何使用 GitHub Actions 自动构建 HTAC 凝汽器计算程序的 Android APK。

---

## 方法一：使用我已配置好的工作流（推荐）

### 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 输入仓库名称，例如：`condenser-calc-android`
3. 选择 **Public**（公开）或 **Private**（私有）
4. 点击 **Create repository**

### 步骤2：上传代码

#### 方式A：通过网页上传

1. 打开新创建的仓库页面
2. 点击 **"uploading an existing file"**
3. 将 `condenser_calc_app_source.zip` 解压后的文件拖放到上传区域
4. 点击 **Commit changes**

#### 方式B：使用Git命令行

```bash
# 解压源码包
unzip condenser_calc_app_source.zip
cd condenser_calc_app

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/condenser-calc-android.git

# 推送代码
git push -u origin main
```

### 步骤3：触发自动构建

1. 代码推送后，GitHub Actions 会自动开始构建
2. 点击仓库顶部的 **Actions** 标签
3. 可以看到正在运行的 **"Build Android APK"** 工作流

### 步骤4：下载APK

#### 方式A：从Artifacts下载

1. 等待构建完成（约10-30分钟）
2. 点击完成的 workflow 运行记录
3. 滚动到底部的 **Artifacts** 部分
4. 点击 **condenser-calc-apk** 下载

#### 方式B：从Release下载（推荐）

1. 构建成功后，会自动创建 Release
2. 点击仓库右侧的 **Releases**
3. 找到最新的 release（如 v1）
4. 下载 APK 文件

---

## 方法二：手动触发构建

### 步骤1：进入Actions页面

1. 打开GitHub仓库
2. 点击 **Actions** 标签
3. 点击左侧的 **Build Android APK**

### 步骤2：运行工作流

1. 点击右侧的 **Run workflow** 按钮
2. 选择分支（通常是 `main` 或 `master`）
3. 点击 **Run workflow**

### 步骤3：等待构建完成

- 构建过程大约需要 10-30 分钟
- 可以在页面上看到实时日志

---

## 方法三：自定义构建配置

### 修改构建参数

编辑 `.github/workflows/build-apk.yml` 文件：

```yaml
# 修改Python版本
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # 修改为需要的版本

# 修改Android架构
android.archs = arm64-v8a  # 只构建64位版本

# 修改API级别
android.api = 34  # Android 14
```

### 添加自定义签名

如果你想使用自己的签名密钥：

1. 生成密钥库：
```bash
keytool -genkey -v -keystore my-key.keystore -alias myalias -keyalg RSA -keysize 2048 -validity 10000
```

2. 将密钥库转为Base64：
```bash
base64 my-key.keystore > my-key.base64
```

3. 在GitHub仓库中添加 Secret：
   - 打开仓库 **Settings** → **Secrets and variables** → **Actions**
   - 点击 **New repository secret**
   - Name: `KEYSTORE_BASE64`
   - Value: 粘贴Base64内容

4. 修改工作流文件：
```yaml
- name: Decode keystore
  run: |
    echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > my-key.keystore
```

---

## 常见问题

### Q1: 构建失败，提示 "No space left on device"

**解决方案**：
- 这是GitHub Actions的免费额度限制
- 尝试只构建一个架构：`android.archs = arm64-v8a`
- 或者使用自托管的runner

### Q2: 构建时间太长

**优化建议**：
- 使用缓存加速构建
- 修改工作流添加缓存：

```yaml
- name: Cache buildozer
  uses: actions/cache@v3
  with:
    path: |
      ~/.buildozer
      ~/.gradle
    key: ${{ runner.os }}-buildozer-${{ hashFiles('buildozer.spec') }}
```

### Q3: 如何修改应用名称和图标

**修改应用名称**：
编辑 `buildozer.spec`：
```ini
title = 你的应用名称
package.name = yourpackagename
package.domain = com.yourcompany
```

**添加图标**：
1. 准备图标文件（512x512 PNG）
2. 放入 `assets/icon.png`
3. 修改 `buildozer.spec`：
```ini
icon.filename = assets/icon.png
```

### Q4: 如何调试构建失败

1. 点击失败的 workflow 运行记录
2. 查看详细的日志输出
3. 常见错误：
   - 依赖缺失：检查 requirements
   - 语法错误：检查 Python 代码
   - 内存不足：减少并行构建任务

---

## 高级配置

### 多架构构建

```yaml
strategy:
  matrix:
    arch: [armeabi-v7a, arm64-v8a]
    
steps:
  - name: Build APK
    run: |
      sed -i 's/android.archs = .*/android.archs = ${{ matrix.arch }}/' buildozer.spec
      buildozer android release
```

### 自动发布到Google Play

需要配置 Google Play API 访问：

```yaml
- name: Upload to Google Play
  uses: r0adkll/upload-google-play@v1
  with:
    serviceAccountJsonPlainText: ${{ secrets.SERVICE_ACCOUNT_JSON }}
    packageName: com.htac.condensercalc
    releaseFiles: bin/*.apk
    track: production
```

### 构建调试版本

```yaml
- name: Build Debug APK
  run: buildozer android debug
```

---

## 完整工作流文件说明

```yaml
name: Build Android APK          # 工作流名称

on:                              # 触发条件
  push:                          # 代码推送时
    branches: [ main, master ]
  pull_request:                  # PR时
    branches: [ main, master ]
  workflow_dispatch:             # 手动触发

jobs:                            # 任务定义
  build-apk:                     # 任务名称
    runs-on: ubuntu-22.04        # 运行环境
    
    steps:                       # 执行步骤
      # 每个 - 是一个步骤
      - name: 步骤名称
        uses: 使用的外部action
        with: 传入的参数
        run:  执行的命令
```

---

## 参考链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Buildozer 文档](https://buildozer.readthedocs.io/)
- [Kivy Android 打包](https://kivy.org/doc/stable/guide/packaging-android.html)

---

## 快速开始检查清单

- [ ] 创建GitHub账号
- [ ] 创建新仓库
- [ ] 上传源码
- [ ] 等待Actions自动构建
- [ ] 下载APK文件
- [ ] 在Android设备上安装测试

**预计总时间**：5分钟设置 + 20分钟构建 = 25分钟获得APK
