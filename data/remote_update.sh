#!/bin/bash

# 配置（请修改）
SERVER="user@server-ip"
REMOTE_PATH="/path/to/server/project"

echo "🚀 开始部署..."

# 同步data目录
echo "📤 同步数据..."
rsync -avz --delete ./data/ "$SERVER:$REMOTE_PATH/data/"

# 执行远程更新
echo "🔄 更新服务器..."
ssh "$SERVER" "cd $REMOTE_PATH && ./update.sh"

echo "✅ 部署完成！"