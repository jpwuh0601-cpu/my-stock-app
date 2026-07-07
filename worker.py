import yfinance as yf
import pandas as pd
import time
import random

def fetch_institutional_data(ticker):
    """
    更新：回傳更接近真實的格式，避免欄位對應錯誤
    """
    # 這裡為您保留測試架構，若您有串接第三方 API，請在此替換邏輯
    return [
        {"日期": "2026-07-06", "外資": 1250, "投信": -300, "自營商": 50},
        {"日期": "2026-07-05", "外資": -800, "投信": 200, "自營商": -120}
    ]

def fetch_top_brokers_data(ticker):
    """
    更新：回傳測試用的券商數據，確保表格格式正確
    """
    data = {
        "券商": ["元大-台北", "凱基-台北", "富邦-總公司"],
        "買賣張數": [450, -210, 150]
    }
    return pd.DataFrame(data)

def fetch_stock_data(ticker):
    """抓取基礎股價資料"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Worker 模組已更新，測試數據架構已完成。")
