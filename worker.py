import yfinance as yf
import pandas as pd
import random

def fetch_stock_data(ticker):
    """抓取股價與財務資料"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # 確保回傳結構穩定
        return {
            "price": info.get("currentPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_real_broker_data(ticker):
    """模擬真實券商數據"""
    return [{"券商": "元大-台北", "買賣張數": 100}, {"券商": "凱基-信義", "買賣張數": -50}]

def fetch_institutional_data(ticker):
    """模擬法人數據"""
    data = {
        "日期": ["近10日平均"],
        "外資": [5000],
        "投信": [1200],
        "自營商": [-300]
    }
    return pd.DataFrame(data)

def fetch_top_brokers_data(ticker):
    """模擬主力券商數據"""
    data = {
        "日期": ["近10日平均"],
        "券商_1": [300],
        "券商_2": [200]
    }
    return pd.DataFrame(data)
