from flask import Flask, request, render_template, redirect, url_for, session
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

app_secret_key = 'b700fe70d5d732756fe1c74774d51b03531f294db364eec7874bd07c5d003e373aab2c0b8a9836a6f5e2e79e6e1139feb7cd783cb451ea9f088dec46eb1dd42ce971c7f3bfaa3353da'

app = Flask(__name__)
app.secret_key = app_secret_key

CLIENT_ID = '113846323534-kl9ij7fdt9shqtviev1uej3rf61r7f8o.apps.googleusercontent.com'
CLIENT_SECRET = "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"

if __name__ == '__main__':
    app = Flask(__name__, template_folder="../templates")
    @app.route('/')
    def index():
        if 'user' in session:
            print("hello2")
            return f'歡迎，{session["user"]}！<br><a href="/logout">登出</a>'
        else:
            print("hello1")
            return render_template("login.html")

@app.route('/login')
def login():
    return redirect(url_for('auth_google'))

@app.route('/auth_google')
def auth_google():
    return redirect(f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri='+request.url_root+'callback&scope=openid%20email%20profile')

@app.route('/callback')
def callback():
    print(request.url_root+'callback')
    code = request.args.get('code')
    token_response = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': request.url_root+'callback',
        'grant_type': 'authorization_code',
    })

    if token_response.status_code == 200:
        token_response_data = token_response.json()
        id_token_response = id_token.verify_oauth2_token(
            token_response_data['id_token'],
            google_requests.Request(),
            CLIENT_ID,
            clock_skew_in_seconds = 60
        )

        # 儲存使用者資訊到 session
        session['user'] = id_token_response['name']
        session['email'] = id_token_response['email']
        return redirect(url_for('index'))
    else:
        return '登入失敗'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
