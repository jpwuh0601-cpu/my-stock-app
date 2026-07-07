import yfinance as yf
import pandas as pd
import time
import random

def fetch_institutional_data(ticker):
    """
    更新：回傳更接近真實的格式，並加入隨機等待，避免被限流
    """
    time.sleep(random.uniform(0.5, 1.5)) # 隨機延遲
    # 這裡為您保留測試架構，若您有串接第三方 API，請在此替換邏輯
    return [
        {"日期": "2026-07-06", "外資": 1250, "投信": -300, "自營商": 50},
        {"日期": "2026-07-05", "外資": -800, "投信": 200, "自營商": -120}
    ]

def fetch_top_brokers_data(ticker):
    """
    更新：回傳測試用的券商數據，確保表格格式正確
    """
    time.sleep(random.uniform(0.5, 1.5))
    data = {
        "券商": ["元大-台北", "凱基-台北", "富邦-總公司"],
        "買賣張數": [450, -210, 150]
    }
    return pd.DataFrame(data)

def fetch_stock_data(ticker):
    """抓取基礎股價資料，加入錯誤預防"""
    try:
        time.sleep(random.uniform(0.5, 1.5))
        stock = yf.Ticker(ticker)
        info = stock.info
        # 如果 info 回傳為空，表示被限流，回傳 error 讓 app.py 處理
        if not info or "regularMarketPrice" not in info and "currentPrice" not in info:
             return {"error": "無法獲取股價資訊，請稍後再試。"}
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": f"資料抓取異常: {str(e)}"}

if __name__ == "__main__":
    print("Canvas 中的 worker.py 模組已完成優化。")
