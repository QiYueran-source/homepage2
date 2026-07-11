#!/bin/bash

# 网站更新脚本
# data 目录已挂载到容器，只需重新生成 html 并重启容器即可

set -e  # 遇到错误立即退出

# 显示当前状态
echo ""
echo "📋 当前容器状态:"
docker compose ps

# 重新生成静态页面
echo ""
echo "🔄 重新生成静态页面..."
docker compose exec homepage python gen.py all

# 重启容器以应用新生成的 html
echo ""
echo "🔄 重启容器..."
docker compose restart homepage

echo ""
echo "✅ 更新完成！"
