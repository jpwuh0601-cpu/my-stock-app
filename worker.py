import json
import logging
import yfinance as yf
import datetime

DATA_FILE = "market_data.json"
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]

def run_analysis_and_update():
    # 準備基本結構，包含時間戳記
    data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for symbol in TICKER_LIST:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        last_price = hist['Close'].iloc[-1] if not hist.empty else 0
        
        data[symbol] = {
            "price": float(last_price),
            "history": [], # 可依需求擴充
            "ai_prediction": "數據已更新。"
        }
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info("數據與時間戳記更新完成")

if __name__ == "__main__":
    run_analysis_and_update()
