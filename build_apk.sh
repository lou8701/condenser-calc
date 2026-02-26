#!/bin/bash
# APK构建脚本

echo "=========================================="
echo "   HTAC凝汽器计算程序 - APK构建"
echo "=========================================="
echo ""

# 检查buildozer是否安装
if ! command -v buildozer &> /dev/null; then
    echo "正在安装buildozer..."
    pip install buildozer cython
fi

# 检查密钥库
KEYSTORE_FILE="htac-release-key.keystore"
if [ ! -f "$KEYSTORE_FILE" ]; then
    echo "签名密钥不存在，正在生成..."
    ./generate_keystore.sh
fi

# 更新buildozer.spec中的签名配置
echo "正在配置签名..."
sed -i "s|# android.keystore =|android.keystore = $KEYSTORE_FILE|" buildozer.spec
sed -i "s|# android.keystore_password =|android.keystore_password = htac123456|" buildozer.spec
sed -i "s|# android.keyalias =|android.keyalias = htac|" buildozer.spec
sed -i "s|# android.keyalias_password =|android.keyalias_password = htac123456|" buildozer.spec

echo ""
echo "开始构建APK..."
echo ""

# 构建发布版APK
buildozer android release

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "   APK构建成功！"
    echo "=========================================="
    echo ""
    echo "APK文件位置: ./bin/*.apk"
    echo ""
    ls -lh ./bin/*.apk 2>/dev/null || echo "请查看 ./bin/ 目录"
else
    echo ""
    echo "APK构建失败！"
    echo "请检查错误信息。"
    exit 1
fi
