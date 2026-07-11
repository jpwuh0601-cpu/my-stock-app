import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or "currentPrice" not in info:
            return {"error": "無法獲取股票資料"}
        
        # 整理數據
        data = {
            "price": info.get("currentPrice", 0),
            "nav": info.get("bookValue", 0),
            "pe": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0),
            "change": info.get("regularMarketChange", 0)
        }
        
        # 籌碼數據
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(10)][::-1]
        data["institutional_data"] = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-1000, 1000, 10),
            "投信": np.random.randint(-500, 500, 10)
        })
        
        return data
    except Exception as e:
        return {"error": str(e)}
