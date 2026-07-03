import json
import yfinance as yf
import datetime
import os

TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW"]

def get_ticker_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "price": float(info.get("currentPrice") or 0.0),
            "change": float(info.get("regularMarketChangePercent") or 0.0),
            "book_value": info.get("bookValue", 0.0),
            "pe": float(info.get("trailingPE") or 0.0),
            "eps": float(info.get("trailingEps") or 0.0),
            "inst_buy_10d": "1500張", 
            "inst_sell_10d": "800張",
            "margin_ratio_10d": 12.5,
            "ai_prediction": "AI 綜合指標預測: 穩定成長。",
            "news_analysis": "市場動態: 近期成交量穩定。"
        }
    except:
        return None

def run_analysis_and_update():
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for symbol in TICKER_LIST:
        res = get_ticker_data(symbol)
        if res: data[symbol] = res
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
