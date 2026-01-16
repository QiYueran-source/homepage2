FROM python:3.9-slim

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统基础工具
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    tree \
    unzip \
    jq \
    net-tools \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 升级pip
RUN python -m pip install --upgrade pip setuptools wheel

# 安装Python开发工具
RUN pip install \
    black \
    flake8 \
    mypy \
    pytest \
    pytest-cov \
    requests \
    beautifulsoup4 \
    jinja2 \
    markdown \
    pyyaml

# 安装Node.js 18 (用于前端工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn prettier

# 创建工作目录
RUN mkdir -p /workspaces
WORKDIR /workspaces

# 创建开发用户
RUN useradd -m -s /bin/bash vscode \
    && chown -R vscode:vscode /workspaces

# 设置环境变量
ENV PYTHONPATH=/workspaces:$PYTHONPATH
ENV PATH=/home/vscode/.local/bin:$PATH

# 切换到开发用户
USER vscode
