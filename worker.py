import json
import yfinance as yf
import datetime
import os

# 包含您需要的股票代號
TICKER_LIST = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "2303.TW", "2308.TW", "6770.TW"]

def run_analysis_and_update():
    # 模擬 10 天數據
    dates = ["06-24", "06-25", "06-26", "06-27", "06-28", "07-01", "07-02", "07-03", "07-04", "07-05"]
    data = {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for symbol in TICKER_LIST:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 建立結構化數據
        data[symbol] = {
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChangePercent", 0),
            "institutional_daily": [{"日期": d, "外資": 1200, "投信": 300, "自營商": -100} for d in dates],
            "broker_daily": [{"日期": d, "主力A": 500, "主力B": 200, "主力C": 50} for d in dates]
        }
    
    # 寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
