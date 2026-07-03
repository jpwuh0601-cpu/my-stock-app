import json
import logging
import yfinance as yf
import datetime
import time
import os

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW"]

def get_ticker_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        time.sleep(2)
        info = ticker.info
        
        # 抓取最近 30 天的歷史數據
        hist = ticker.history(period="1mo")
        # 將歷史數據轉換為列表格式，適合寫入 JSON
        history_list = []
        for date, row in hist.iterrows():
            history_list.append({
                "date": date.strftime("%Y-%m-%d"),
                "close": float(row["Close"])
            })

        return {
            "price": float(info.get("currentPrice") or info.get("regularMarketPrice") or 0.0),
            "history": history_list,
            "eps": float(info.get("trailingEps") or 0.0),
            "pe": float(info.get("trailingPE") or 0.0),
            "ai_prediction": "數據已同步更新，包含一個月歷史走勢。"
        }
    except Exception as e:
        return {"price": 0.0, "history": [], "ai_prediction": "數據獲取失敗"}

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for symbol in TICKER_LIST:
        data[symbol] = get_ticker_data(symbol)
            
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
