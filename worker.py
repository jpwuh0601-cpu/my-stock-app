import json
import yfinance as yf
import datetime
import pandas as pd
import os

# 監控清單
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW"]

def get_籌碼屬性(張數):
    return "大戶" if abs(張數) >= 400 else "散戶"

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        # 產生最近 10 天的日期作為每日細項範例
        dates = pd.date_range(end=datetime.datetime.now(), periods=10).strftime("%Y-%m-%d").tolist()
        
        # 模擬法人每日細項
        inst_daily = [{"日期": d, "外資": 1200, "投信": 300, "自營商": -150} for d in dates]
        
        # 模擬券商每日細項 (含大戶/散戶屬性)
        broker_daily = [
            {"日期": d, "券商": "凱基-台北", "買賣超(張)": 550, "屬性": get_籌碼屬性(550)} 
            for d in dates
        ]
        
        data[symbol] = {
            "price": yf.Ticker(symbol).info.get("currentPrice", 0),
            "change": yf.Ticker(symbol).info.get("regularMarketChangePercent", 0),
            "institutional_daily": inst_daily,
            "broker_daily": broker_daily
        }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
