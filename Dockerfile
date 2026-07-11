# 单阶段构建：Python 轻量静态服务
# 容器内不再包含 Nginx，由宿主机 Nginx 统一处理反向代理和 SSL
FROM python:3.9-slim

WORKDIR /app

# 复制依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码、模板和生成脚本
COPY . .

# 创建 html 输出目录
RUN mkdir -p /app/html

# 暴露服务端口
EXPOSE 83

# 启动时根据挂载的 data 生成 html，并启动静态文件服务
CMD ["sh", "-c", "python gen.py all && uvicorn serve:app --host 0.0.0.0 --port 83"]