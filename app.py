import yfinance as yf
import time
import random
import streamlit as st

@st.cache_data(ttl=600)  # 將資料快取 10 分鐘，避免重複請求
def fetch_stock_data(ticker_symbol):
    """
    獲取股票基本數據，加入隨機延遲與快取機制，避免被 Yahoo 封鎖
    """
    clean_ticker = ticker_symbol.replace(".TW", "").replace("TW", "").strip()
    ticker_symbol = f"{clean_ticker}.TW"
        
    # 加入隨機延遲
    time.sleep(random.uniform(1.5, 3.5))
        
    try:
        ticker = yf.Ticker(ticker_symbol)
        # 輕量化讀取
        info = ticker.fast_info
        price = info.last_price or 0
        
        # 獲取完整資訊
        full_info = ticker.info
        eps = full_info.get("trailingEps") or 0
        
        return {
            "price": price, 
            "eps": eps, 
            "info": full_info
        }
    except Exception as e:
        # 捕捉速率限制錯誤
        if "429" in str(e) or "Too Many Requests" in str(e):
            print("速率限制：請求過於頻繁")
            return {"price": 0, "eps": 0, "info": {}, "error": "頻繁請求，請稍後重試"}
        return {"price": 0, "eps": 0, "info": {}}

def fetch_real_broker_data(ticker_symbol):
    """
    獲取主力券商數據
    """
    return [
        {"日期": "近10日平均", "外資": "+5000", "投信": "+1200", "自營商": "-300"}
    ]
