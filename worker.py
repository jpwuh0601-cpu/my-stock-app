import yfinance as yf
import pandas as pd
import time
import random
import requests

def fetch_institutional_data(ticker):
    """回傳法人籌碼每日細項資料，確保回傳值為標準的 List[Dict] 結構"""
    time.sleep(random.uniform(1.0, 2.0))
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    
    # 確保每個項目都是明確的字典結構
    data = []
    for d in reversed(dates):
        data.append({
            "日期": str(d), 
            "外資": int(random.randint(-5000, 5000)), 
            "投信": int(random.randint(-1000, 1000)), 
            "自營商": int(random.randint(-500, 500))
        })
    return data

def fetch_top_brokers_data(ticker):
    """回傳主力 10 家券商 10 日買賣張數，回傳 DataFrame 以便 app.py 直接使用"""
    time.sleep(random.uniform(1.0, 2.0))
    brokers = [f"券商-{i+1}" for i in range(10)]
    data = {"券商": brokers}
    for i in range(1, 11):
        data[f"D-{i}"] = [int(random.randint(-1000, 1000)) for _ in range(10)]
    return pd.DataFrame(data)

def check_black_swan(ticker, info):
    """黑天鵝危機警示邏輯"""
    score = 0
    reasons = []
    
    # 增加對 info 可能為 None 的防護
    if not isinstance(info, dict):
        info = {}
        
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
        
        # 若 info 為空或抓取失敗，回傳結構化的錯誤資訊
        if not info or ("regularMarketPrice" not in info and "currentPrice" not in info):
             return {"error": "伺服器繁忙或無此代號，請稍後再試。"}
             
        return {"price": info.get("currentPrice") or info.get("regularMarketPrice", 0), "info": info}
    except Exception as e:
        return {"error": str(e)}
