#!/bin/bash

# 配置（请修改）
SERVER="user@server-ip"
REMOTE_PATH="/path/to/server/project"

echo "🚀 开始部署..."

# 同步 data 目录到服务器
# 由于服务器端已挂载 data 目录，同步后只需重启容器即可生效
echo "📤 同步数据..."
rsync -avz --delete ./data/ "$SERVER:$REMOTE_PATH/data/"

# 执行远程更新（重新生成 html 并重启容器，无需重建镜像）
echo "🔄 更新服务器..."
ssh "$SERVER" "cd $REMOTE_PATH && ./update.sh"

echo "✅ 部署完成！"