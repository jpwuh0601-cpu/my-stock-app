import yfinance as yf
import pandas as pd
import time
import random
import requests

def fetch_institutional_data(ticker):
    """回傳法人籌碼每日細項資料，確保數據類型統一"""
    time.sleep(random.uniform(1.0, 2.0))
    # 模擬 10 日法人資料，強制確保數值為整數
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    return [
        {
            "日期": d, 
            "外資": int(random.randint(-5000, 5000)), 
            "投信": int(random.randint(-1000, 1000)), 
            "自營商": int(random.randint(-500, 500))
        }
        for d in reversed(dates)
    ]

def fetch_top_brokers_data(ticker):
    """回傳主力 10 家券商 10 日買賣張數，確保格式為數值"""
    time.sleep(random.uniform(1.0, 2.0))
    brokers = [f"券商-{i+1}" for i in range(10)]
    data = {"券商": brokers}
    for i in range(1, 11):
        # 確保所有買賣張數均為整數
        data[f"D-{i}"] = [int(random.randint(-1000, 1000)) for _ in range(10)]
    return pd.DataFrame(data)

def check_black_swan(ticker, info):
    """黑天鵝危機警示邏輯"""
    score = 0
    reasons = []
    # 使用 safe_float 概念處理潛在的字串或 None
    debt = float(info.get('debtToEquity', 0) or 0)
    profit = float(info.get('profitMargins', 0) or 0)
    
    if debt > 200: 
        score += 30; reasons.append("負債比過高")
    if profit < 0: 
        score += 40; reasons.append("營收虧損中")
    
    status = "安全" if score < 30 else "⚠️ 警示中"
    return status, reasons

def fetch_stock_data(ticker):
    """偽裝瀏覽器抓取基礎股價"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    try:
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        if not info or ("regularMarketPrice" not in info and "currentPrice" not in info):
             return {"error": "伺服器繁忙，請稍後再試。"}
        return {"price": info.get("currentPrice") or info.get("regularMarketPrice", 0), "info": info}
    except Exception as e:
        return {"error": str(e)}
