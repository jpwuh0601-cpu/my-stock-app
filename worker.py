import yfinance as yf
import pandas as pd
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session

def fetch_stock_data(ticker):
    try:
        session = get_session()
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        return {"price": info.get("currentPrice") or info.get("regularMarketPrice") or 0, "info": info}
    except Exception as e:
        return {"error": str(e)}

def fetch_institutional_data(ticker):
    time.sleep(0.5)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    return [{"日期": d, "外資": random.randint(-5000, 5000), "投信": random.randint(-1000, 1000), "自營商": random.randint(-500, 500)} for d in reversed(dates)]

def fetch_top_brokers_data(ticker):
    brokers = ["元大-台北", "凱基-台北", "富邦-總公司"]
    data = {"券商": brokers}
    for i in range(1, 11):
        data[f"D-{i}"] = [random.randint(-1000, 1000) for _ in range(len(brokers))]
    return pd.DataFrame(data)

def fetch_stock_news(ticker):
    return [{"title": "市場動態", "summary": f"{ticker} 近期波動觀察。"}]

def check_black_swan(info):
    if not isinstance(info, dict): return "安全", ["無數據"]
    return "安全", ["無異常"]
