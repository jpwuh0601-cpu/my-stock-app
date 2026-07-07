import yfinance as yf
import pandas as pd
import time
import random
import requests
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session

def fetch_institutional_data(ticker):
    """模擬法人籌碼數據"""
    time.sleep(0.5)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    return [{"日期": d, "外資": random.randint(-5000, 5000), "投信": random.randint(-1000, 1000), "自營商": random.randint(-500, 500)} for d in reversed(dates)]

def fetch_top_brokers_data(ticker):
    """模擬主力券商數據"""
    return pd.DataFrame({"券商": ["元大-台北", "凱基-台北"], "D-1": [100, -50]})

def calculate_indicators(df):
    if df.empty or len(df) < 26:
        return {"KD": "資料不足", "MACD": "資料不足", "RSI": "資料不足"}
    close = df['Close']
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    rsv = (close - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return {"KD": f"K:{k.iloc[-1]:.2f}, D:{d.iloc[-1]:.2f}", "MACD": f"快線:{macd.iloc[-1]:.2f}, 訊號線:{signal.iloc[-1]:.2f}", "RSI": f"{rsi.iloc[-1]:.2f}"}

def fetch_stock_data(ticker):
    try:
        session = get_session()
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        hist = stock.history(period="1mo")
        indicators = calculate_indicators(hist)
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        return {"price": price, "info": info, **indicators}
    except Exception as e:
        return {"error": str(e)}

def check_black_swan(info):
    if not isinstance(info, dict): return "資料異常", ["無法解析"]
    debt = float(info.get('debtToEquity', 0) or 0)
    profit = float(info.get('profitMargins', 0) or 0)
    status = "安全" if debt < 200 and profit >= 0 else "⚠️ 警示中"
    return status, ["財務風險評估"]
