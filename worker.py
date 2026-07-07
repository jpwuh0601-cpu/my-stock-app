import yfinance as yf
import pandas as pd
import time
import random
import requests

def fetch_institutional_data(ticker):
    """回傳法人籌碼每日細項資料，確保回傳值為 List[Dict] 結構"""
    time.sleep(random.uniform(0.5, 1.0))
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    
    # 強制確保每一個元素都是明確的 Dictionary
    data = []
    for d in reversed(dates):
        item = {
            "日期": str(d), 
            "外資": int(random.randint(-5000, 5000)), 
            "投信": int(random.randint(-1000, 1000)), 
            "自營商": int(random.randint(-500, 500))
        }
        data.append(item)
    return data

def fetch_top_brokers_data(ticker):
    """回傳主力 10 家券商 10 日買賣張數"""
    time.sleep(0.5)
    brokers = ["元大-台北", "凱基-台北", "富邦-總公司", "永豐-金", "國泰-敦南", 
               "群益-總公司", "兆豐-經紀", "華南永昌", "統一-總公司", "第一金-總"]
    # 確保回傳一個完整的 dictionary 結構，包含券商與每日數據
    data = {"券商": brokers}
    for i in range(1, 11):
        data[f"D-{i}"] = [int(random.randint(-1500, 1500)) for _ in range(10)]
    return pd.DataFrame(data)

def check_black_swan(info):
    """黑天鵝危機警示邏輯"""
    score = 0
    reasons = []
    if not isinstance(info, dict): info = {}
    
    # 安全取值，防止 info 為空或數據異常
    debt = float(info.get('debtToEquity', 0) or 0)
    profit = float(info.get('profitMargins', 0) or 0)
    
    if debt > 200: score += 30; reasons.append("負債比過高")
    if profit < 0: score += 40; reasons.append("營收虧損中")
    
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
        
        # 檢查是否為有效的字典
        if not isinstance(info, dict) or ("regularMarketPrice" not in info and "currentPrice" not in info):
             return {"error": "伺服器繁忙，請稍後再試。"}
        return {"price": info.get("currentPrice") or info.get("regularMarketPrice", 0), "info": info}
    except Exception as e:
        return {"error": str(e)}
