import json
import yfinance as yf
import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

# 這裡擴充您要查詢的股票
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW"]

def get_ticker_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 模擬法人與籌碼數據 (實際應用建議串接 CMoney 或 XQ API)
        return {
            "price": float(info.get("currentPrice") or 0.0),
            "change_price": float(info.get("regularMarketChange") or 0.0),
            "change_percent": float(info.get("regularMarketChangePercent") or 0.0),
            "book_value": info.get("bookValue", 0.0),
            "pe": float(info.get("trailingPE") or 0.0),
            "eps": float(info.get("trailingEps") or 0.0),
            "inst_buy_10d": "1250張", # 三大法人
            "broker_buy_10d": "主力券商A: 500張, B: 300張", # 10家券商
            "margin_ratio_10d": 15.5,
            "ai_prediction": "綜合指標預測: 穩定。",
            "news_analysis": "市場觀察: 買盤集中於主力券商。"
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
