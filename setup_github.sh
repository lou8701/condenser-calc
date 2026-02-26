#!/bin/bash
# GitHub Actions 一键设置脚本

echo "=========================================="
echo "  HTAC凝汽器计算 - GitHub Actions 设置"
echo "=========================================="
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    echo "错误: 未找到 git，请先安装"
    exit 1
fi

# 获取GitHub用户名
echo "请输入你的GitHub用户名:"
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "错误: GitHub用户名不能为空"
    exit 1
fi

# 获取仓库名
echo "请输入仓库名称 (默认: condenser-calc):"
read -r REPO_NAME
REPO_NAME=${REPO_NAME:-condenser-calc}

echo ""
echo "配置信息:"
echo "  GitHub用户名: $GITHUB_USERNAME"
echo "  仓库名称: $REPO_NAME"
echo "  完整地址: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "确认创建? (y/n)"
read -r CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "已取消"
    exit 0
fi

# 初始化git
echo ""
echo "[1/5] 初始化Git仓库..."
git init
git add .
git commit -m "Initial commit: HTAC condenser calculator"

# 添加远程仓库
echo "[2/5] 添加远程仓库..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# 推送代码
echo "[3/5] 推送代码到GitHub..."
echo "  提示: 如果提示输入密码，请使用GitHub Personal Access Token"
git push -u origin main 2>/dev/null || git push -u origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "[4/5] 推送成功!"
    echo ""
    echo "=========================================="
    echo "  设置完成!"
    echo "=========================================="
    echo ""
    echo "GitHub Actions 将自动开始构建APK"
    echo ""
    echo "查看构建状态:"
    echo "  https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
    echo ""
    echo "下载APK (构建完成后):"
    echo "  https://github.com/$GITHUB_USERNAME/$REPO_NAME/releases"
    echo ""
    echo "预计构建时间: 15-30分钟"
    echo ""
else
    echo ""
    echo "[4/5] 推送失败!"
    echo ""
    echo "可能的原因:"
    echo "  1. 仓库不存在，请先创建:"
    echo "     https://github.com/new"
    echo "  2. 认证失败，请检查用户名和密码/Token"
    echo ""
    echo "手动推送命令:"
    echo "  git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "  git push -u origin main"
    echo ""
fi

echo "[5/5] 完成!"
echo ""
