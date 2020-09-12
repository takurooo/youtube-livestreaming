# -----------------------------
# import
# -----------------------------
import os
import json
import pickle

from google.auth.transport.requests import Request
import google_auth_oauthlib

import user

# -----------------------------
# define
# -----------------------------
# SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
SCOPES = ["https://www.googleapis.com/auth/youtube"]

API_KEY = json.load(open(user.API_KEY_PATH, "r"))["api_key"]
CLIENT_SECRET = user.CLIENT_SECRETS_PATH
TOKEN_FILE = user.TOKEN_PATH
# -----------------------------
# function
# -----------------------------
def get_apikey():
    return API_KEY

def get_credentials():

    credentials = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)

    if credentials and credentials.valid:
        print("credentials valid")
        return credentials

    if credentials and credentials.expired and credentials.refresh_token:
        # リフレッシュトークンフロー(RFC 6749,6)
        print("refresh token flow")
        credentials.refresh(Request())
    else:
        # 認可エンドポイントへ 認可リクエスト
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET,
                    SCOPES,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                )
    
        # ユーザー認証画面の表示
        auth_url, _ = flow.authorization_url(prompt='consent')

        print("")
        print('please go to this URL: {}'.format(auth_url))
        print("")

        # 認可コード取得
        code = input('Enter the authorization code: ')

        # トークンエンドポイントへ アクセストークン要求
        flow.fetch_token(code=code)

        # アクセストークン取得
        credentials = flow.credentials

    # アクセストークンを保存
    with open(TOKEN_FILE, 'wb') as token_file:
        pickle.dump(credentials, token_file)
        

    return credentials