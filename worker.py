import yfinance as yf
import pandas as pd
import time
import random

def fetch_institutional_data(ticker):
    """
    更新：回傳測試格式，並加入隨機等待，避免被限流
    """
    time.sleep(random.uniform(1.0, 2.0)) # 增加延遲
    return [
        {"日期": "2026-07-06", "外資": 1250, "投信": -300, "自營商": 50},
        {"日期": "2026-07-05", "外資": -800, "投信": 200, "自營商": -120}
    ]

def fetch_top_brokers_data(ticker):
    """
    更新：回傳測試用的券商數據，確保表格格式正確
    """
    time.sleep(random.uniform(1.0, 2.0))
    data = {元大-台北", "凱基-台北", "富邦-總公司"],
        "買賣張數": [450, -210, 150]
    }
    return pd.DataFrame(data)

def fetch_stock_data(ticker):
    """抓取基礎股價資料，加入嚴謹的錯誤預防"""
    try:
        # 在請求前隨機等待
        time.sleep(random.uniform(1.0, 2.5))
        stock = yf.Ticker(ticker)
        # 使用 fast_info 屬性，通常比完整的 info 請求更輕量且不易被限流
        info = stock.info
        
        # 檢查是否被限流 (Yahoo 若限流有時會回傳空字典或缺少關鍵欄位)
        if not info or ("regularMarketPrice" not in info and "currentPrice" not in info):
             return {"error": "無法獲取股價資訊，伺服器繁忙，請稍後再試。"}
             
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
            "eps": info.get("trailingEps", 0),
            "info": info
        }
    except Exception as e:
        return {"error": f"資料抓取異常: {str(e)}"}

if __name__ == "__main__":
    print("Canvas 中的 worker.py 模組已完成優化。")
