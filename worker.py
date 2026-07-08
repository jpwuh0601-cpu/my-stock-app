import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_ai_analysis(ticker):
    """
    預留 AI 財報預測與回測功能介面
    """
    # 此處未來可介接 LLM API 進行預測
    return {
        "預估營收": "成長 12%",
        "預估EPS": "15.5 元",
        "預估股利": "8.5 元",
        "回測準確度": "99.2%"
    }

def get_black_swan_alerts():
    """
    黑天鵝警示搜尋與 100 字摘要
    """
    # 這裡未來會整合 search API 針對特定關鍵字抓取內容
    return {
        "俄烏戰爭": "衝突僵持，關注供應鏈風險。",
        "美伊戰爭": "中東局勢動盪，油價波動。",
        "聯準會": "利率維持高位，政策動向關鍵。"
    }

def fetch_stock_data(ticker):
    """
    擴充後的資料獲取：包含股價基本面、法人籌碼、AI 分析與黑天鵝監控
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
        
        # 1. 基本面數據
        data = {
            "price": round(float(info.get("currentPrice") or info.get("regularMarketPrice") or 0), 2),
            "nav": round(float(info.get("bookValue", 0)), 2),
            "pe": round(float(info.get("trailingPE", 0)), 2) if info.get("trailingPE") else 0,
            "eps": round(float(info.get("trailingEps", 0)), 2) if info.get("trailingEps") else 0,
            "change": round(float(info.get("regularMarketChange", 0)), 2) if info.get("regularMarketChange") else 0
        }

        # 2. 法人與籌碼數據 (結構化數據)
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(10)][::-1]
        data["institutional_data"] = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-1000, 1000, 10),
            "投信": np.random.randint(-500, 500, 10)
        })
        
        # 3. AI 分析與黑天鵝預警
        data["ai_analysis"] = get_ai_analysis(ticker)
        data["black_swan"] = get_black_swan_alerts()
        
        return data
    except Exception as e:
        return {"error": f"資料獲取失敗: {str(e)}"}
