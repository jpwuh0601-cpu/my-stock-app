import json
import logging
import yfinance as yf
import datetime
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

# 這裡加入您所有需要追蹤的股票
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW", "2412.TW"]

def get_ticker_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        time.sleep(1)
        info = ticker.info
        
        # 取得歷史資料
        hist = ticker.history(period="10d")
        
        return {
            "price": float(info.get("currentPrice") or info.get("regularMarketPrice") or 0.0),
            "change": float(info.get("regularMarketChangePercent") or 0.0),
            "book_value": info.get("bookValue", 0.0),
            "pe": float(info.get("trailingPE") or 0.0),
            "eps": float(info.get("trailingEps") or 0.0),
            "est_revenue": "待估算",
            "est_eps": "待估算",
            "est_dividend": "待估算",
            "inst_buy_10d": "資料處理中",
            "inst_sell_10d": "資料處理中",
            "margin_ratio_10d": 15.2,
            "ai_prediction": "綜合指標：趨勢中性，建議觀察外資買賣超。",
            "news_analysis": "近期市場反應熱絡，相關供應鏈表現穩定。"
        }
    except Exception as e:
        return None

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for symbol in TICKER_LIST:
        res = get_ticker_data(symbol)
        if res: data[symbol] = res
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
