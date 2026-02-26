#!/bin/bash
# 生成签名密钥脚本

KEYSTORE_FILE="htac-release-key.keystore"
KEY_ALIAS="htac"
VALIDITY_DAYS=10000

# 检查是否已存在密钥库
if [ -f "$KEYSTORE_FILE" ]; then
    echo "密钥库已存在: $KEYSTORE_FILE"
    exit 0
fi

echo "=========================================="
echo "   HTAC凝汽器计算程序 - 签名密钥生成"
echo "=========================================="
echo ""
echo "正在生成签名密钥..."
echo ""

# 生成密钥库
keytool -genkey -v \
    -keystore "$KEYSTORE_FILE" \
    -alias "$KEY_ALIAS" \
    -keyalg RSA \
    -keysize 2048 \
    -validity "$VALIDITY_DAYS" \
    -dname "CN=HTAC, OU=Engineering, O=HTAC, L=Beijing, ST=Beijing, C=CN" \
    -storepass htac123456 \
    -keypass htac123456

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "   签名密钥生成成功！"
    echo "=========================================="
    echo ""
    echo "密钥库文件: $KEYSTORE_FILE"
    echo "密钥别名: $KEY_ALIAS"
    echo "有效期: $VALIDITY_DAYS 天"
    echo ""
    echo "密钥库密码: htac123456"
    echo "密钥密码: htac123456"
    echo ""
    echo "请妥善保管此密钥文件！"
else
    echo ""
    echo "密钥生成失败！"
    exit 1
fi
