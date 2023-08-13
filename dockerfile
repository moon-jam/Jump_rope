# 使用官方的 Python 基礎映像
FROM python:3.11.4
# FROM panda0322/jump_rope_web

# 將專案中的所有檔案複製到容器中的 /app 目錄
COPY . /app

# 設定工作目錄
WORKDIR /app

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gevent gunicorn
RUN pip install mediapipe

# 定義容器啟動時要運行的命令
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-t", "86400"]
