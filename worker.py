import yfinance as yf
import pandas as pd
import time

# 加入全局緩存字典，減少 API 請求
_cache = {}

def fetch_stock_data(ticker):
    """加入強制間隔與簡單快取，防止被鎖 IP"""
    if ticker in _cache:
        return _cache[ticker]
    
    try:
        # 強制延遲，這是防止被封鎖最有效的手段
        time.sleep(2.0)
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 檢查關鍵欄位
        if 'currentPrice' not in info:
            return {"error": "API 暫時繁忙，請稍後再試。"}
            
        result = {
            "price": info.get("currentPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
        _cache[ticker] = result
        return result
    except Exception as e:
        return {"error": str(e)}

def fetch_real_broker_data(ticker):
    return [{"券商": "元大-台北", "買賣張數": 100}, {"券商": "凱基-信義", "買賣張數": -50}]

def fetch_institutional_data(ticker):
    return pd.DataFrame({"日期": ["近10日"], "外資": [5000], "投信": [1200], "自營商": [-300]})

def fetch_top_brokers_data(ticker):
    return pd.DataFrame({"日期": ["近10日"], "券商_1": [300], "券商_2": [200]})
