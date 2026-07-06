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
    # 針對 429 和常見的伺服器錯誤進行重試，backoff_factor 會讓每次等待時間指數成長
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    # 使用真實的瀏覽器 User-Agent
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    })
    return session

def fetch_stock_data(ticker):
    """抓取 Yahoo Finance 資料，加入隨機延遲與重試機制"""
    # 每次呼叫強制隨機延遲 3 到 7 秒，避免觸發 Yahoo 防護機制
    time.sleep(random.uniform(3, 7)) 
    
    try:
        session = get_session()
        stock = yf.Ticker(ticker, session=session)
        
        # 獲取基礎資料
        info = stock.info
        
        # 檢查關鍵欄位是否存在
        if not info or ('currentPrice' not in info and 'regularMarketPrice' not in info):
            return {"error": "資料擷取受限 (Rate Limited)，請稍後再試。"}
            
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": f"系統錯誤: {str(e)}"}

def fetch_institutional_data(ticker):
    """抓取法人買賣超數據 (使用證交所格式)"""
    try:
        stock_id = ticker.replace(".TW", "")
        url = f"https://www.twse.com.tw/rwd/zh/fund/T86?selectType=ALL&stockID={stock_id}"
        session = get_session()
        response = session.get(url, timeout=15)
        data = response.json()
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'], columns=['日期', '代號', '名稱', '外陸資買賣超', '投信買賣超', '自營商買賣超', '合計'])
            return df.tail(5)[['日期', '外陸資買賣超', '投信買賣超', '自營商買賣超']]
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def fetch_top_brokers_data(ticker):
    """主力券商統計模擬"""
    return pd.DataFrame({
        "券商": ["元大-台北", "凱基-信義", "富邦-嘉義"],
        "買賣張數": [100, -50, 20]
    })

if __name__ == "__main__":
    print("Worker 模組已優化並準備就緒。")
