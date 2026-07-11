import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    """
    獲取股票資訊並進行異常處理，確保數據穩定輸出。
    並加入十日法人買賣超數據模擬邏輯。
    """
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 增加更嚴謹的檢查：確保 info 不為 None 且包含關鍵欄位
        if not info or "currentPrice" not in info:
            return {"error": f"無法獲取股票 {ticker} 的資料，請確認代號是否正確。"}
        
        # 整理數據 (使用 .get 避免 Key Error)
        data = {
            "price": info.get("currentPrice", 0.0),
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "change": info.get("regularMarketChange", 0.0)
        }
        
        # 獲取最近 10 個交易日的歷史數據，模擬法人買賣超數據
        hist = stock.history(period="10d")
        
        # 產生十日法人買賣超明細
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
        # 捕捉所有連線或解析異常
        return {"error": f"發生系統錯誤: {str(e)}"}
