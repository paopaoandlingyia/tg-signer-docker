FROM python:3.11.2-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制程序文件
COPY signer.py .
COPY my_account.session .

# 设置时区
ENV TZ=Asia/Shanghai

# 运行程序
CMD ["python", "signer.py"]