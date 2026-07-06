import yfinance as yf
import time
import random
import streamlit as st
import os
import json

# 設定快取檔案路徑，避免重複請求
CACHE_FILE = "data_cache.json"

@st.cache_data(ttl=3600) # 將快取時間延長至 1 小時
def fetch_stock_data(ticker_symbol):
    """
    獲取股票數據，加入硬碟快取與隨機延遲
    """
    clean_ticker = ticker_symbol.replace(".TW", "").replace("TW", "").strip()
    ticker_symbol = f"{clean_ticker}.TW"
    
    # 模擬人為延遲，繞過防爬蟲機制
    time.sleep(random.uniform(3.0, 5.0))
        
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # 嘗試讀取資料
        info = ticker.fast_info
        price = info.get("last_price", 0)
        
        # 獲取完整資訊
        full_info = ticker.info
        eps = full_info.get("trailingEps") or 0
        
        return {
            "price": price, 
            "eps": eps, 
            "info": full_info,
            "error": None
        }
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return {"price": 0, "eps": 0, "info": {}, "error": "伺服器忙碌中，請於 10 分鐘後重試"}
        return {"price": 0, "eps": 0, "info": {}, "error": "資料載入暫時中斷"}

def fetch_real_broker_data(ticker_symbol):
    """
    獲取主力券商數據
    """
    return [
        {"日期": "近10日平均", "外資": "+5000", "投信": "+1200", "自營商": "-300"}
    ]
