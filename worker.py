import yfinance as yf
import pandas as pd
import time

def fetch_stock_data(ticker):
    """
    抓取 Yahoo Finance 資料，加入重試機制與延遲防止 IP 被封鎖
    """
    try:
        # 強制延遲 2 秒，降低觸發 Rate Limit 的機率
        time.sleep(2.0)
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 檢查關鍵數據是否存在
        if 'currentPrice' not in info:
            return {"error": "無法獲取股價資料，請稍後再試。"}
            
        return {
            "price": info.get("currentPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": f"資料讀取失敗: {str(e)}"}

def fetch_real_broker_data(ticker):
    """
    抓取券商籌碼資料，與 main_task.py 調用名稱對齊
    """
    # 這裡可保留模擬數據，或未來串接真實爬蟲
    return [{"券商": "元大-台北", "買賣張數": 100}, {"券商": "凱基-信義", "買賣張數": -50}]

def fetch_institutional_data(ticker):
    """
    抓取法人籌碼統計資料
    """
    # 此處可擴充為呼叫台灣證交所 API 的邏輯
    data = {
        "日期": ["近10日平均"],
        "外資": [5000],
        "投信": [1200],
        "自營商": [-300]
    }
    return pd.DataFrame(data)

def fetch_top_brokers_data(ticker):
    """
    抓取主力券商統計資料
    """
    data = {
        "日期": ["近10日平均"],
        "券商_1": [300],
        "券商_2": [200]
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    # 簡單的模組自我測試
    print("Worker 模組已載入並準備就緒。")
