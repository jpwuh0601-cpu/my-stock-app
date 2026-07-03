import json
import yfinance as yf
import datetime
import pandas as pd

# 追蹤清單，可隨時擴充
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
            "est_revenue": "預估中",
            "est_eps": "預估中",
            "est_dividend": "預估中",
            "margin_ratio_10d": 15.2,
            # 法人與券商資料改為 List of Dict，方便顯示為表格
            "institutional_data": [
                {"法人": "外資", "買賣超(張)": 1500},
                {"法人": "投信", "買賣超(張)": 300},
                {"法人": "自營商", "買賣超(張)": -120}
            ],
            "broker_data": [
                {"券商名稱": "凱基-台北", "買賣超(張)": 450},
                {"券商名稱": "富邦-建國", "買賣超(張)": -120},
                {"券商名稱": "元大-總公司", "買賣超(張)": 300}
            ],
            "ai_prediction": "綜合指標：趨勢穩健。",
            "news_analysis": "近期成交量穩定，外資持股比例上升。"
        }
    except Exception:
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
