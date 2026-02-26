#!/bin/bash
# 使用python-for-android构建APK

export PATH="/home/kimi/.local/bin:$PATH"

# 检查依赖
echo "检查依赖..."
which p4a || { echo "p4a not found"; exit 1; }

# 创建构建目录
mkdir -p build

# 使用p4a构建
echo "开始构建APK..."
p4a apk \
    --private . \
    --package=com.htac.condensercalc \
    --name "HTAC凝汽器计算" \
    --version 1.0.0 \
    --bootstrap=sdl2 \
    --requirements=python3,kivy \
    --arch=arm64-v8a \
    --android-api=33 \
    --ndk-api=21 \
    --orientation=portrait \
    --icon=assets/icon.png \
    --presplash=assets/presplash.png \
    --release \
    --sign \
    --keystore=htac-release-key.keystore \
    --alias=htac \
    --keystorepw=htac123456 \
    --aliaspw=htac123456 \
    --dist_name=condensercalc \
    2>&1

echo "构建完成！"
