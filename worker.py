import os
import requests
import twstock
import pandas as pd
import logging
import json
import yfinance as yf
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker):
    """加入錯誤處理與超時機制"""
    try:
        # 使用 yfinance 取代不穩定的 twstock
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="5d")
        if hist.empty: return {"ticker": ticker, "error": "無資料"}
        
        current_price = hist['Close'].iloc[-1]
        return {"ticker": ticker, "price": f"{current_price:.2f}", "status": "ok"}
    except Exception as e:
        logging.error(f"Error fetching {ticker}: {e}")
        return {"ticker": ticker, "error": "數據異常"}

def send_line_message(content):
    """推送訊息"""
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    
    if not token or not user_id:
        logging.error("LINE 設定缺失")
        return
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"to": user_id, "messages": [{"type": "text", "text": content}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        logging.info(f"LINE 推送狀態: {response.status_code}")
    except Exception as e:
        logging.error(f"LINE 推送異常: {e}")

if __name__ == "__main__":
    watchlist = os.getenv("WATCHLIST", "2330,2881").split(",")
    report_data = [fetch_stock_data(t) for t in watchlist]
    msg = f"每日股市健檢完成:\n{json.dumps(report_data, ensure_ascii=False)}"
    send_line_message(msg)
