import json
import logging
import yfinance as yf
import datetime
import time
import os

logging.basicConfig(level=logging.INFO)

# 明確獲取檔案路徑，確保與 app.py 在同一目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]

def get_ticker_data(symbol):
    ticker = yf.Ticker(symbol)
    time.sleep(3) 
    info = ticker.info
    return {
        "price": float(ticker.fast_info.last_price or 0),
        "eps": float(info.get("trailingEps") or 0),
        "pe": float(info.get("trailingPE") or 0),
        "ai_prediction": "數據已同步更新。"
    }

def run_analysis_and_update():
    logging.info(f"正在將資料寫入至: {DATA_FILE}")
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for symbol in TICKER_LIST:
        data[symbol] = get_ticker_data(symbol)
            
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("資料寫入完成。")

if __name__ == "__main__":
    run_analysis_and_update()
