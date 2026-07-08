import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    """
    擴充後的資料獲取：包含股價基本面與模擬法人籌碼數據
    """
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        
        # 基本面數據
        data = {
            "price": round(float(info.get("currentPrice") or info.get("regularMarketPrice") or 0), 2),
            "nav": round(float(info.get("bookValue", 0)), 2),
            "pe": round(float(info.get("trailingPE", 0)), 2) if info.get("trailingPE") else 0,
            "eps": round(float(info.get("trailingEps", 0)), 2) if info.get("trailingEps") else 0,
            "change": round(float(info.get("regularMarketChange", 0)), 2) if info.get("regularMarketChange") else 0
        }

        # 模擬法人與資券數據 (真實來源串接點)
        # 後續可將此處替換為向公開財經網站爬取的真實 HTML 表格解析
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(10)][::-1]
        data["institutional_data"] = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-1000, 1000, 10),
            "投信": np.random.randint(-500, 500, 10)
        })
        data["margin_data"] = pd.DataFrame({
            "日期": dates,
            "資券比": [round(np.random.uniform(5, 20), 2) for _ in range(10)]
        })
        
        return data
    except Exception as e:
        return {"error": f"資料獲取失敗: {str(e)}"}
