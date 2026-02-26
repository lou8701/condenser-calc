[app]
# 应用标题
title = HTAC凝汽器计算

# 包名
package.name = condensercalc

# 包域名
package.domain = com.htac

# 源文件目录
source.dir = .

# 版本号
version = 1.0.0

#  requirements
requirements = python3,kivy

# 图标
# icon.filename = assets/icon.png

# 启动图片
# presplash.filename = assets/presplash.png

# 架构
android.archs = armeabi-v7a,arm64-v8a

# API级别
android.api = 33

# 最低API级别
android.minapi = 21

# NDK API级别
android.ndk_api = 21

# SDK路径（自动检测）
# android.sdk_path = 

# NDK路径（自动检测）
# android.ndk_path = 

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 屏幕方向
orientation = portrait

# 全屏
fullscreen = 0

# 日志级别
android.logcat_filters = *:S python:D

# 签名配置
android.keystore = htac-release-key.keystore
android.keystore_password = htac123456
android.keyalias = htac
android.keyalias_password = htac123456 

[buildozer]
# 日志级别
log_level = 2

# 警告模式
warn_on_root = 1
