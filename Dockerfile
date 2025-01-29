FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装基础工具
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装VPN客户端
RUN curl -sSL https://client.alioss.net/install.sh | bash

# 复制项目文件
COPY requirements.txt .
COPY main.py .
COPY .env.example .env

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建下载目录
RUN mkdir -p downloads

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动命令
CMD ["python", "main.py"] 