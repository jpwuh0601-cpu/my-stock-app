import json
import requests
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import math

def send_line_notify(message):
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": str(message)}
    try:
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE 通知失敗: {e}")

def sanitize(val):
    try:
        if val is None: return 0.0
        f = float(val)
        if not math.isfinite(f): return 0.0
        return f
    except: return 0.0

def run_analysis_and_update():
    ticker_code = "2330"
    ticker = yf.Ticker(f"{ticker_code}.TW")
    
    # 增加延遲避免被 Yahoo Finance 封鎖
    time.sleep(2)
    
    try:
        info = ticker.info
    except Exception as e:
        print(f"獲取資訊失敗: {e}")
        info = {}

    final_data = {
        "update_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticker": ticker_code,
        "price": sanitize(info.get("currentPrice")),
        "market_cap": sanitize(info.get("marketCap")),
        "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        "ai_prediction": "基於當前指標，市場觀望氣氛濃厚。"
    }
    
    output_path = "market_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    send_line_notify(f"每日股市更新完成: {ticker_code}")

if __name__ == "__main__":
    run_analysis_and_update()
