import json
import yfinance as yf
import datetime
import pandas as pd
import os

# 初始清單，若您輸入新的代號，系統會自動抓取
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW", "6770.TW"]

def get_籌碼屬性(張數):
    return "大戶" if abs(張數) >= 400 else "散戶"

def run_analysis_and_update():
    dates = pd.date_range(end=datetime.datetime.now(), periods=10).strftime("%m-%d").tolist()
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 產生數據
        data[symbol] = {
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChangePercent", 0),
            "institutional_daily": [{"日期": d, "外資(張)": 1000, "投信(張)": 200} for d in dates],
            "broker_daily": [{"日期": d, "主力A(張)": 500, "主力B(張)": 300} for d in dates]
        }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
