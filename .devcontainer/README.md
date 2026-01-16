# Dev Container 开发环境

本项目支持使用VS Code Dev Containers进行远程开发。

## 🚀 快速开始

### 前提条件
1. 安装 [VS Code](https://code.visualstudio.com/)
2. 安装 [Dev Containers扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 使用方法
1. 打开项目文件夹
2. 按 `Ctrl+Shift+P` (或 `Cmd+Shift+P` 在Mac上)
3. 选择 "Dev Containers: Reopen in Container"
4. 等待容器构建完成（首次需要几分钟）

## 🔧 开发环境特性

### 基础镜像
- **Python 3.9-slim** - Python官方精简镜像
- **基于Debian** - 轻量级Linux系统
- **非root用户** - 使用vscode用户进行开发

### 已安装工具
- **Python 3.9** - 主要开发语言
- **pip** - Python包管理器
- **black** - 代码格式化
- **flake8** - 代码检查
- **Node.js 18** - 前端工具支持
- **yarn** - Node包管理器
- **Git** - 版本控制
- **curl/wget** - 网络工具

### VS Code扩展
- Python
- Black Formatter
- Flake8
- JSON/YAML支持
- Tailwind CSS IntelliSense
- Docker支持
- Prettier

### 挂载配置
- 项目根目录完全挂载到容器内
- 修改文件立即在容器中生效
- 支持热重载开发

## 📝 开发命令

```bash
# 生成所有页面
python gen.py all

# 只生成首页
python gen.py home

# 生成特定模块
python gen.py blog
python gen.py project
python gen.py docs

# 本地预览（开发用）
python -m http.server 8000

# 启动生产预览服务
docker-compose --profile preview up -d

# 停止预览服务
docker-compose --profile preview down
```

## 🌐 访问服务

- **开发预览**: http://localhost:8000 (本地HTTP服务器)
- **生产预览**: http://localhost:8081 (公网端口，内部转发到容器80端口)

## 🔄 工作流程

1. **开发**: 修改代码文件
2. **生成**: 运行 `python gen.py all` 生成静态文件
3. **预览**: 访问 http://localhost:8000 查看效果
4. **部署**: 使用 `docker-compose up -d` 部署到生产

## 🐛 故障排除

### 容器无法启动
```bash
# 查看容器状态
docker-compose ps

# 查看容器日志
docker-compose logs dev
docker-compose logs homepage

# 重启开发环境
docker-compose restart dev
```

### 端口冲突
如果8081或8000端口被占用：
1. 关闭占用端口的程序
2. 或修改端口映射

### 依赖安装失败
```bash
# 手动安装依赖
pip install -r requirements.txt

# 更新pip
python -m pip install --upgrade pip
```

## 📚 更多信息

- [Dev Containers 文档](https://code.visualstudio.com/docs/devcontainers/containers)
- [VS Code 远程开发](https://code.visualstudio.com/docs/remote/remote-overview)
