#!/bin/bash

# 网站更新脚本
# 用于重新构建镜像并重启容器

set -e  # 遇到错误立即退出

# 显示当前状态
echo ""
echo "📋 当前容器状态:"
docker-compose ps

# 停止当前运行的容器
echo ""
echo "🛑 停止当前容器..."
docker-compose down

# 清理未使用的镜像（可选）
echo ""
echo "🧹 清理未使用的Docker镜像..."
docker image prune -f

# 重新构建镜像并启动容器
echo ""
echo "🔨 重新构建镜像..."
docker-compose build --no-cache

echo ""
echo "🏃 启动新容器..."
docker-compose up -d
echo "✅ 更新完成！"
