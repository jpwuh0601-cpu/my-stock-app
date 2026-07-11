import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    """
    獲取股票資訊並進行異常處理，確保數據穩定輸出。
    加入十日法人買賣超與十家主力券商買賣超模擬數據，並優化數值呈現格式。
    """
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        # 強制等待並取得資訊
        info = stock.info
        
        # 【關鍵修復】檢查 info 是否為空，如果為 None 或空字典，回傳錯誤資訊
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
            data["broker_data"] = pd.DataFrame(columns=["日期", "元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"])
        else:
            institutional_data = []
            broker_data = []
            for date, row in hist.iterrows():
                date_str = date.strftime('%m-%d')
                
                # 法人數據：隨機產生並加入正負標記邏輯
                institutional_data.append({
                    "日期": date_str,
                    "外資": np.random.randint(-1500, 1500),
                    "投信": np.random.randint(-800, 800),
                    "自營商": np.random.randint(-500, 500)
                })
                
                # 模擬十家主力券商數據
                broker_vals = {
                    "日期": date_str,
                    "元大": np.random.randint(-500, 500), "凱基": np.random.randint(-500, 500),
                    "富邦": np.random.randint(-500, 500), "永豐金": np.random.randint(-500, 500),
                    "國泰": np.random.randint(-500, 500), "群益": np.random.randint(-500, 500),
                    "元富": np.random.randint(-500, 500), "華南": np.random.randint(-500, 500),
                    "兆豐": np.random.randint(-500, 500), "統一": np.random.randint(-500, 500)
                }
                broker_data.append(broker_vals)
                
            data["institutional_data"] = pd.DataFrame(institutional_data)
            data["broker_data"] = pd.DataFrame(broker_data)
        
        return data
        
    except Exception as e:
        return {"error": f"連線異常，請稍後再查: {str(e)}"}
