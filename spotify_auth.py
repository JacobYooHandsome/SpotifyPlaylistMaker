from bs4 import BeautifulSoup
import requests
import os
import webbrowser
import base64
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
refresh_token = os.getenv("REFRESH_TOKEN")

auth_string = client_id + ":" + client_secret
auth_bytes = auth_string.encode('utf-8')
auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
access_token = ''

headers = {
    "Authorization": 'Basic ' + auth_base64,
    'Content-Type':'application/x-www-form-urlencoded',
}

def request_access():
    sp_auth = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri" : redirect_uri,
    "scope" : "playlist-modify-public",
    }
    url = "https://accounts.spotify.com/authorize?" + "&".join([f"{k}={v}" for k, v in sp_auth.items()])
    webbrowser.open(url)

def request_token(token):
    sp_access = {
        "grant_type":"authorization_code",
        "code":token,
        "redirect_uri":redirect_uri
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=sp_access, headers=headers)
    print(response.json())

def refresh_token():
    sp_refresh = {
        "grant_type":"refresh_token",
        "refresh_token":"AQB_eCCzLXUBOPI8Cb4vrbHibDF-WHh_9LfSZ6f1bkx6fjFps9jtC27tbwysIHMYMB90tpF_gFpWWPdzq9jpFZ4CqoopVukEsFQiXYg9x8ACB0P3NVMyTYOJUDMk8b4Cko4"
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=sp_refresh, headers=headers)
    print(response.json())
    global access_token 
    access_token = response.json()["access_token"]

def get_token():
    return access_token