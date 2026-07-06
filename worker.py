import yfinance as yf
import pandas as pd
import time
import requests
from io import StringIO

def fetch_stock_data(ticker):
    """抓取 Yahoo Finance 資料，加入延遲機制"""
    time.sleep(3) 
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if info is None or 'currentPrice' not in info:
            return {"error": "API 頻繁呼叫限制中，請稍後再試。"}
        return {"price": info.get("currentPrice", 0), "eps": info.get("trailingEps", 0), "info": info}
    except Exception as e:
        return {"error": f"資料讀取失敗: {str(e)}"}

def fetch_institutional_data(ticker):
    """
    階段 A：抓取真實法人買賣超數據 (使用證交所公開資料)
    """
    try:
        # 移除 .TW 以符合證交所代號格式
        stock_id = ticker.replace(".TW", "")
        url = f"https://www.twse.com.tw/rwd/zh/fund/T86?selectType=ALL&stockID={stock_id}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            # 簡化資料處理，取最後幾筆展示
            df = pd.DataFrame(data['data'], columns=['日期', '代號', '名稱', '外陸資買賣超', '投信買賣超', '自營商買賣超', '合計'])
            # 僅回傳前端需要的三大欄位
            return df.tail(5)[['日期', '外陸資買賣超', '投信買賣超', '自營商買賣超']]
        else:
            raise ValueError("查無資料")
    except:
        # 若抓取失敗回傳空表
        return pd.DataFrame({"日期": ["無資料"], "外陸資買賣超": [0], "投信買賣超": [0], "自營商買賣超": [0]})

def fetch_top_brokers_data(ticker):
    """主力券商數據 (保留基礎結構)"""
    return pd.DataFrame({"券商": ["元大-台北", "凱基-信義"], "買賣張數": [100, -50]})

if __name__ == "__main__":
    print("Worker 模組已更新為真實數據源模式。")
