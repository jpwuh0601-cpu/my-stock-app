import yfinance as yf
import pandas as pd
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    """建立帶有重試機制的 session，避免 Too Many Requests 錯誤"""
    session = requests.Session()
    # 增加重試次數與延遲因子
    retry = Retry(connect=5, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"})
    return session

def fetch_stock_data(ticker):
    """獲取股票基礎資訊"""
    try:
        session = get_session()
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        hist = stock.history(period="1mo")
        # 確保價格獲取有容錯
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        return {"price": price, "info": info}
    except Exception as e:
        return {"error": f"資料獲取異常: {str(e)}"}

def fetch_institutional_data(ticker):
    """模擬法人籌碼數據"""
    time.sleep(0.5)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%Y-%m-%d').tolist()
    return [{"日期": d, "外資": random.randint(-5000, 5000), "投信": random.randint(-1000, 1000), "自營商": random.randint(-500, 500)} for d in reversed(dates)]

def fetch_top_brokers_data(ticker):
    """模擬主力券商數據"""
    time.sleep(0.5)
    brokers = ["元大-台北", "凱基-台北", "富邦-總公司", "永豐-金", "國泰-敦南"]
    data = {"券商": brokers}
    for i in range(1, 11):
        data[f"D-{i}"] = [random.randint(-1500, 1500) for _ in range(len(brokers))]
    return pd.DataFrame(data)

def fetch_stock_news(ticker):
    """抓取簡單新聞"""
    return [{"title": "市場即時動態", "summary": f"{ticker} 近期交易維持常態波動。"}]

def check_black_swan(info):
    """檢查財務風險"""
    if not isinstance(info, dict):
        return "安全", ["無數據"]
    debt = float(info.get('debtToEquity', 0) or 0)
    profit = float(info.get('profitMargins', 0) or 0)
    # 簡單的風險邏輯
    status = "安全" if debt < 200 and profit >= 0 else "⚠️ 警示中"
    return status, ["財務風險評估"]

if __name__ == "__main__":
    # 測試用邏輯
    print(fetch_stock_data("2330.TW"))
