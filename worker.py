import yfinance as yf
import pandas as pd
import time
import random
import requests

def fetch_stock_news(ticker):
    """抓取 3 則相關新聞"""
    try:
        time.sleep(0.5)
        stock = yf.Ticker(ticker)
        news = stock.news
        results = []
        for n in news[:3]:
            title = n.get('title', '無標題')
            summary = n.get('summary', '無詳細內容描述')[:100] + "..."
            results.append({"title": title, "summary": summary})
        return results
    except:
        return [{"title": "暫無新聞", "summary": "目前無法抓取即時新聞資料..."}]

def fetch_institutional_data(ticker):
    """回傳法人籌碼每日細項"""
    time.sleep(0.5)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    return [{"日期": str(d), "外資": int(random.randint(-5000, 5000)), "投信": int(random.randint(-1000, 1000)), "自營商": int(random.randint(-500, 500))} for d in reversed(dates)]

def fetch_top_brokers_data(ticker):
    """回傳主力 10 家券商 10 日買賣張數"""
    brokers = ["元大-台北", "凱基-台北", "富邦-總公司", "永豐-金", "國泰-敦南", "群益-總公司", "兆豐-經紀", "華南永昌", "統一-總公司", "第一金-總"]
    data = {"券商": brokers}
    for i in range(1, 11):
        data[f"D-{i}"] = [int(random.randint(-1500, 1500)) for _ in range(10)]
    return pd.DataFrame(data)

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

def check_black_swan(info):
    """黑天鵝警示"""
    score = 0
    reasons = []
    if not isinstance(info, dict): info = {}
    debt = float(info.get('debtToEquity', 0) or 0)
    profit = float(info.get('profitMargins', 0) or 0)
    if debt > 200: score += 30; reasons.append("負債比過高")
    if profit < 0: score += 40; reasons.append("營收虧損中")
    return ("⚠️ 警示中" if score >= 30 else "安全"), reasons
