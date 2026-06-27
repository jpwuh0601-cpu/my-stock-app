import twstock
import pandas as pd
import random
import requests
import os
from datetime import datetime
from dotenv import load_dotenv  # 新增：用於載入 .env 檔案

# 載入環境變數 (優先讀取 .env 檔案)
load_dotenv()

# 設定參數：若未設定環境變數則給予警告
LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
if not LINE_TOKEN:
    print("警告：未偵測到 LINE_NOTIFY_TOKEN，通知功能將無法運作。")

# ... (其餘 fetch_data, ai_score 等邏輯保持不變)

def send_line_message(message):
    if not LINE_TOKEN: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)
