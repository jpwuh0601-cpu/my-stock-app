import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    ticker = ticker.strip().upper()
    # 確保代號正確 (加上 .TW)
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        # 強制等待並取得資訊
        info = stock.info
        
        # 【關鍵修復】檢查 info 是否為空，如果為 None 或空字典，回傳錯誤資訊而不是崩潰
        if not info or not isinstance(info, dict) or "currentPrice" not in info:
            return {"error": f"無法獲取代號 {ticker} 的股市資訊，請稍後再試。"}
        
        # 整理數據 (使用安全的 .get)
        data = {
            "price": info.get("currentPrice", 0.0),
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "change": info.get("regularMarketChange", 0.0)
        }
        
        # 生成十日法人買賣超模擬數據
        hist = stock.history(period="10d")
        if hist.empty:
            data["institutional_data"] = pd.DataFrame(columns=["日期", "外資", "投信", "自營商"])
        else:
            institutional_data = []
            for date, row in hist.iterrows():
                institutional_data.append({
                    "日期": date.strftime('%m-%d'),
                    "外資": np.random.randint(-1500, 1500),
                    "投信": np.random.randint(-800, 800),
                    "自營商": np.random.randint(-500, 500)
                })
            data["institutional_data"] = pd.DataFrame(institutional_data)
        
        return data
        
    except Exception as e:
        return {"error": f"連線異常，請稍後再查: {str(e)}"}
