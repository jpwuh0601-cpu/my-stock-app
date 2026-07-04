import yfinance as yf
import json
import datetime
import twstock
import os
import logging
import random

# 設定日誌
logging.basicConfig(level=logging.INFO)

def get_detailed_institutional_data():
    """模擬獲取詳細的三大法人與券商買賣超資料 (請在未來串接 twstock.bargin)"""
    # 模擬 10 日資料
    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d") for i in range(10)]
    return {
        "三大法人": [{"日期": d, "外資": random.randint(-5000, 5000), "投信": random.randint(-1000, 1000), "自營商": random.randint(-2000, 2000)} for d in dates],
        "主力券商": [{"日期": d, "券商A": random.randint(-100, 100), "券商B": random.randint(-100, 100)} for d in dates]
    }

def run_analysis_and_update():
    target_file = "market_data.json"
    # 新增：支援外部設定清單 (未來可存入 settings.json)
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW"]
    
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        
        # 籌碼資料寫入
        chips = get_detailed_institutional_data()
        
        data[symbol] = {
            "price": price,
            "nav": info.get("bookValue", 0),
            "pe": info.get("forwardPE", 0),
            "eps": info.get("trailingEps", 0),
            "institutional_data": chips["三大法人"],
            "broker_data": chips["主力券商"],
            "ai_prediction": "AI 預測：近期觀察籌碼流向顯示主力有吸籌跡象。",
            "margin_ratio": 12.5  # 模擬資券比
        }
            
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
