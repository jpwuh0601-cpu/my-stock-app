import yfinance as yf
import pandas as pd
import time
import requests
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    """建立具備自動重試功能的 requests session"""
    session = requests.Session()
    # 增加重試機制，針對 429 錯誤進行指數退避
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    })
    return session

def fetch_stock_data(ticker):
    """抓取 Yahoo Finance 資料，加入隨機延遲與重試"""
    time.sleep(random.uniform(2, 5)) # 強制隨機延遲
    try:
        session = get_session()
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        
        # 檢查資料完整性
        if not info or 'currentPrice' not in info:
            return {"error": "資料獲取受限 (Rate Limited)，請稍後再試。"}
            
        return {
            "price": info.get("currentPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": f"系統錯誤: {str(e)}"}
