import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    """
    抓取 Yahoo Finance 的個股資料
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "price": info.get("currentPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_real_broker_data(ticker):
    """
    模擬券商分析數據，確保與 main_task.py 中的調用相容
    """
    # 這裡未來可替換為真實的網路爬蟲程式碼
    return [{"券商": "元大-台北", "買賣張數": 100}, {"券商": "凱基-信義", "買賣張數": -50}]

def fetch_institutional_data(ticker):
    """
    抓取法人籌碼數據
    """
    data = {
        "日期": ["近10日平均"],
        "外資": [5000],
        "投信": [1200],
        "自營商": [-300]
    }
    return pd.DataFrame(data)

def fetch_top_brokers_data(ticker):
    """
    抓取主力券商數據
    """
    data = {
        "日期": ["近10日平均"],
        "券商_1": [300],
        "券商_2": [200]
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    # 測試代碼，確保 worker 本身執行沒問題
    print("Worker 模組載入正常")
