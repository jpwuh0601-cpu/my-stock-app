import os
import requests
import logging
import yfinance as yf
from datetime import datetime

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker):
    """抓取最新價格並格式化"""
    try:
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="1d")
        if hist.empty: return f"{ticker}: 無資料"
        
        price = hist['Close'].iloc[-1]
        # 加入簡單的漲跌幅計算 (假設與前一日相比)
        return f"【{ticker}】現價: {price:.2f}"
    except Exception as e:
        return f"{ticker}: 數據異常"

def send_line_message(content):
    """推送結構化訊息至 LINE"""
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    
    if not token or not user_id:
        logging.error("LINE 設定缺失")
        return
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"to": user_id, "messages": [{"type": "text", "text": content}]}
    
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        logging.error(f"LINE 推送異常: {e}")

if __name__ == "__main__":
    watchlist = os.getenv("WATCHLIST", "2330,2881").split(",")
    results = [fetch_stock_data(t) for t in watchlist]
    
    # 將原始數據改為易讀的格式
    msg = f"🌅 每日股市晨報 ({datetime.now().strftime('%Y-%m-%d')}):\n\n" + "\n".join(results)
    send_line_message(msg)
