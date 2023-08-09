# 使用一個基本的 Python 映像作為基底
FROM python:3.8-slim

# 設定環境變數
ENV FLASK_APP=app.py

# 在容器內建立一個目錄來儲存你的專案
WORKDIR /app

# 複製專案檔案到容器內
COPY . /app

# 安裝相依套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放指定的埠號
EXPOSE 8000

# 執行 Gunicorn 伺服器
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
