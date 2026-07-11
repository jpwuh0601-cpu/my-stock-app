import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    """
    獲取股票資訊並進行異常處理，確保數據穩定輸出。
    優化券商買賣超數據格式，加入趨勢標記以利前端呈現。
    """
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 檢查 info 是否為空
        if not info or not isinstance(info, dict) or "currentPrice" not in info:
            return {"error": f"無法獲取代號 {ticker} 的股市資訊，請稍後再試。"}
        
        # 整理數據
        data = {
            "price": info.get("currentPrice", 0.0),
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "change": info.get("regularMarketChange", 0.0)
        }
        
        # 生成十日法人與券商模擬數據
        hist = stock.history(period="10d")
        if hist.empty:
            data["institutional_data"] = pd.DataFrame(columns=["日期", "外資", "投信", "自營商"])
            data["broker_data"] = pd.DataFrame(columns=["日期", "元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"])
        else:
            institutional_data = []
            broker_data = []
            
            for date, row in hist.iterrows():
                date_str = date.strftime('%m-%d')
                
                # 法人數據
                institutional_data.append({
                    "日期": date_str,
                    "外資": np.random.randint(-1500, 1500),
                    "投信": np.random.randint(-800, 800),
                    "自營商": np.random.randint(-500, 500)
                })
                
                # 券商數據：將值與趨勢標記分開，方便前端處理
                brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
                b_vals = {"日期": date_str}
                for b in brokers:
                    val = np.random.randint(-500, 500)
                    # 這裡我們傳遞整數值，前端再根據此數值判斷顏色
                    b_vals[b] = val
                broker_data.append(b_vals)
                
            data["institutional_data"] = pd.DataFrame(institutional_data)
            data["broker_data"] = pd.DataFrame(broker_data)
        
        return data
        
    except Exception as e:
        return {"error": f"連線異常，請稍後再查: {str(e)}"}
