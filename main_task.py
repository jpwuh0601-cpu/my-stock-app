import json
import os
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}
    
    for ticker in tickers:
        stock = fetch_stock_data(ticker)
        final_results[ticker] = {
            "price": stock.get("price", 0),
            "nav": stock.get("info", {}).get("bookValue", 0),
            "pe": stock.get("info", {}).get("trailingPE", 0),
            "eps": stock.get("eps", 0),
            "ai_report": "分析中..."
        }
    
    # 強制寫入到當前執行目錄的根目錄
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("檔案已寫入: market_data.json")

if __name__ == "__main__":
    run_main()
