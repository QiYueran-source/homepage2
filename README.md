# 个人主页项目

一个基于Python和Jinja2的静态网站生成器，用于生成个人主页。

## 🚀 快速开始

### 使用Docker部署（推荐）

```bash
# 1. 构建镜像
docker build -t homepage .

# 2. 运行容器
docker run -p 8081:8081 homepage

# 或者使用docker-compose
docker-compose up -d
```

### 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 生成网站
python gen.py all

# 3. 预览（可选）
python -m http.server 8000 -d html
```

## 🌐 访问网站

- Docker部署: `http://localhost:8081` (公网端口，内部转发到容器80端口)
- 本地开发: `http://localhost:8000`

访问根路径会自动显示主页（home.html）。

## 📁 项目结构

```
├── data/              # 数据文件
│   ├── blog/         # 博客文章
│   ├── project/      # 项目信息
│   ├── docs/         # 文档资源
│   ├── stack/        # 技术栈
│   └── contact/      # 联系方式
├── scripts/          # 生成脚本
├── templates/        # Jinja2模板
├── html/            # 生成的静态文件
├── Dockerfile       # Docker构建文件
├── nginx.conf       # Nginx配置
└── gen.py          # 主生成脚本
```

## 🛠️ 可用命令

```bash
# 生成所有内容
python gen.py all

# 仅生成博客
python gen.py blog

# 仅生成项目
python gen.py project

# 仅生成文档
python gen.py docs

# 仅生成技术栈
python gen.py stack

# 仅生成联系方式
python gen.py contact

# 生成主页
python gen.py home
```

## 📦 Docker特性

- **多阶段构建**: 优化镜像大小（~20MB）
- **端口映射**: 8081端口访问
- **自动重定向**: 根路径自动跳转到home.html
- **静态文件服务**: 使用Nginx提供高性能服务
- **健康检查**: 自动检测服务状态

## 🔧 自定义配置

### 修改端口
在`docker-compose.yml`中修改端口映射：
```yaml
ports:
  - "8081:8081"  # 修改为其他端口
```

### 自定义Nginx配置
编辑`nginx.conf`文件来调整Nginx配置。

## 📝 开发说明

### 添加新博客
1. 在`data/blog/分类名/`下创建文章目录
2. 添加`card.json`和`content.md`文件
3. 运行`python gen.py blog`

### 添加新项目
1. 在`data/project/`下创建项目目录
2. 添加`card.json`和`content.md`文件
3. 运行`python gen.py project`

### 修改样式
编辑`templates/`目录下的模板文件，然后重新生成。

## 📄 许可证

本项目采用MIT许可证。
