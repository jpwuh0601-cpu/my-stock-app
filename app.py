import yfinance as yf
import time
import random
import streamlit as st

@st.cache_data(ttl=600)  # 將資料快取 10 分鐘，避免重複請求
def fetch_stock_data(ticker_symbol):
    """
    獲取股票基本數據，加入隨機延遲與快取機制，避免被 Yahoo 封鎖
    """
    # 確保格式正確
    clean_ticker = ticker_symbol.replace(".TW", "").replace("TW", "").strip()
    ticker_symbol = f"{clean_ticker}.TW"
        
    # 加入隨機延遲，分散請求壓力 (隨機延遲拉長以避開連續請求)
    time.sleep(random.uniform(2.0, 4.0))
        
    try:
        # 增加連線嘗試的安全性
        ticker = yf.Ticker(ticker_symbol)
        
        # 使用 fast_info 屬性，此屬性更輕量且不易受 API 速率限制影響
        info = ticker.fast_info
        price = info.get("last_price", 0)
        
        # 獲取完整資訊 (加入錯誤捕獲)
        # 若 info 獲取失敗，我們給予預設值以維持頁面運作
        full_info = ticker.info if hasattr(ticker, 'info') else {}
        eps = full_info.get("trailingEps") or 0
        
        return {
            "price": price, 
            "eps": eps, 
            "info": full_info,
            "error": None
        }
    except Exception as e:
        # 捕捉速率限制與連線錯誤
        error_msg = str(e)
        if "429" in error_msg or "Too Many Requests" in error_msg:
            return {"price": 0, "eps": 0, "info": {}, "error": "請求過於頻繁 (429)，請稍候再試"}
        if "404" in error_msg:
            return {"price": 0, "eps": 0, "info": {}, "error": "找不到股票代號"}
            
        return {"price": 0, "eps": 0, "info": {}, "error": f"連線錯誤: {error_msg[:20]}"}

def fetch_real_broker_data(ticker_symbol):
    """
    獲取主力券商數據 (模擬資料)
    """
    return [
        {"日期": "近10日平均", "外資": "+5000", "投信": "+1200", "自營商": "-300"}
    ]
