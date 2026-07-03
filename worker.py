import json
import yfinance as yf
import datetime
import os

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW"]

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 籌碼與財務預估結構
        data[symbol] = {
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChangePercent", 0),
            "change_val": info.get("regularMarketChange", 0),
            "book_value": info.get("bookValue", 0),
            "pe": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0),
            "est_revenue": "1.2兆", # 模擬預估值
            "est_eps": "42.5",
            "est_dividend": "25.0",
            "margin_ratio": 15.2, # 10日資券比
            "institutional_data": [{"項目": "外資", "10日買賣超": 5000}, {"項目": "投信", "10日買賣超": 1200}, {"項目": "自營商", "10日買賣超": -800}],
            "broker_data": [{"券商": "凱基", "10日買賣": 300}, {"券商": "元大", "10日買賣": -150}],
            "ai_report": "基本面穩定，技術面籌碼集中。",
            "news": "近期市場動態：半導體龍頭獲利穩健。"
        }
        
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
