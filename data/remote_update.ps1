# 以管理员权限运行执行权限  
# set-executionpolicy remotesigned 

# 配置（请修改）
$SERVER = "user@server-ip"
$REMOTE_PATH = "/path/to/server/project"

Write-Host "🚀 开始部署..."

# 同步data目录
Write-Host "📤 同步数据..."
ssh "$SERVER" "rm -rf $REMOTE_PATH/data/*"
scp -r ../data/* "$SERVER`:$REMOTE_PATH/data/"

# 执行远程更新
Write-Host "🔄 更新服务器..."
ssh "$SERVER" "cd $REMOTE_PATH && ./update.sh"

Write-Host "✅ 部署完成！"
Write-Host "按任意键退出..." -NoNewline
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")