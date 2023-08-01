import os
import json  # 導入 json 模組
from datetime import datetime
from flask import Flask, request, render_template, send_file, redirect, url_for, session
import threading

import vision_detect
import auth

app = Flask(__name__)
app.secret_key = auth.app_secret_key

# 設定上傳檔案和處理檔案的資料夾路徑
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

def load_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        return render_template("login.html")

@app.route('/upload', methods=['POST'])
def upload():
    # 確認請求中是否包含名為'video'的檔案部分
    if 'video' not in request.files:
        return "No file part"
    
    # 取得使用者上傳的影片檔案
    video_file = request.files['video']

    # 確認使用者是否選擇了檔案
    if video_file.filename == '':
        return "No selected file"

    # 使用當前日期時間來建立新的檔名
    current_datetime = datetime.now()
    filename = current_datetime.strftime("%Y%m%d%H%M%S")+ '_' + video_file.filename

    # 將使用者上傳的影片儲存到伺服器上的暫存位置
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_file.save(video_path)

    # 處理影片，並將處理過後的影片儲存到指定資料夾
    processed_filename = "processed_" + filename
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    process_thread = threading.Thread(target=vision_detect.process_video, args=(video_path, processed_path,))

    process_thread.start()
    # 重新導向到下載頁面，並將處理過後的影片檔案名稱作為查詢參數
    return redirect(url_for('result_page', video=processed_filename))

# 設置新的路由來處理下載頁面
@app.route('/result_page')
def result_page():
    # 取得查詢參數中的影片檔案名稱
    video_name = request.args.get('video')
    # 回傳 download.html 模板，並將影片檔案名稱傳遞到模板中
    return render_template('result.html', video_name=video_name)

# 設置新的路由來處理下載影片
@app.route('/download/<video>')
def download(video):
    # 取得處理過後的影片檔案路徑
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], video)
    # 以檔案下載方式回傳影片檔案
    return send_file(processed_path, as_attachment=True, download_name="processed_" + processed_path[35:])

@app.route('/download_original/<video>')
def download_original(video):
    # 取得原始影片檔案路徑
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], video)
    # 以檔案下載方式回傳原始影片檔案
    return send_file(original_path, as_attachment=True, download_name=original_path[23:])

# 新增影片列表路由
@app.route('/video_list')
def video_list():
    # 取得上傳影片的檔案列表
    uploaded_videos = os.listdir(app.config['UPLOAD_FOLDER'])
    processed_videos = os.listdir(app.config['PROCESSED_FOLDER'])

    video_list_info = []

    for video in uploaded_videos:
        processed_filename = 'processed_' + video
        filename = os.path.splitext(video)[0]
        json_filename = 'processed_' + filename + '.json'
        
        time_str = filename.split("_")[0]
        name_str = filename.split("_")[1]
        
        upload_time = datetime.strptime(time_str, '%Y%m%d%H%M%S')  # 轉換成 datetime 物件
        formatted_upload_time = upload_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式化成 'yyyy-mm-dd HH:MM'
        
        if json_filename in processed_videos:
            json_path = os.path.join(app.config['PROCESSED_FOLDER'], json_filename)
            with open(json_path, 'r') as f:
                video_info = json.load(f)
                video_list_info.append({
                    'video_name': name_str,
                    'upload_time': formatted_upload_time,
                    'times': video_info['times'],
                    'score': video_info['score'],
                    'rank': video_info['rank'],
                    'full_filename': video
                })
        else:
            video_list_info.append({
                'video_name': name_str,
                'upload_time': formatted_upload_time,
                'times': 'Processing...',
                'score': 'Processing...',
                'rank': 'Processing...',
                'full_filename': video
            })

    # 回傳 video_list.html 模板，並將影片列表資訊傳遞到模板中
    return render_template('video_list.html', video_list_info=video_list_info)

@app.route('/login')
def login():
    return redirect(url_for('auth_google'))

@app.route('/auth_google')
def auth_google():
    return auth.auth_google()

@app.route('/callback')
def callback():
    return auth.callback()

@app.route('/logout')
def logout():
    return auth.logout()

if __name__ == '__main__':
    app.run(debug=True)
