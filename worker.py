import json
import yfinance as yf
import datetime
import pandas as pd
import pandas_ta as ta

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW"]

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")
        # 計算技術指標
        hist['RSI'] = ta.rsi(hist['Close'], length=14)
        
        info = ticker.info
        data[symbol] = {
            "price": info.get("currentPrice", 0),
            "prev_close": info.get("previousClose", 0),
            "diff": round(info.get("currentPrice", 0) - info.get("previousClose", 0), 2),
            "pe": info.get("forwardPE", 0),
            "eps": info.get("trailingEps", 0),
            "ai_prediction": "AI 偵測到近期外資買盤強勁，技術面呈現黃金交叉。",
            "institutional_daily": [{"日期": "07-03", "外資": 5000, "投信": 200, "自營商": -100}],
            "broker_daily": [{"日期": "07-03", "主力A": 1000, "主力B": 500}]
        }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
