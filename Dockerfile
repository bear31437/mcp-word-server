# 使用Python 3.9作為基底環境
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製程式碼進容器
COPY mcp_server.py .

# 安裝需要的套件
RUN pip install flask python-docx pandas

# 開放5005 port
EXPOSE 5005

# 啟動服務
CMD ["python", "mcp_server.py"]