# 多阶段构建：第一阶段生成静态文件
FROM python:3.9-slim as builder

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 生成静态网站
RUN python gen.py all

# 第二阶段：使用Nginx提供服务
FROM nginx:alpine

# 复制自定义nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 复制生成的静态文件到Nginx目录
COPY --from=builder /app/html /usr/share/nginx/html

# 暴露端口8081
EXPOSE 8081

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]