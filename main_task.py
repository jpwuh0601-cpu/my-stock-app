import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    for ticker in tickers:
        print(f"正在處理: {ticker}")
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        
        final_results[ticker] = {
            "price": stock_info.get("price", 0),
            "nav": 0, "pe": 0, "eps": stock_info.get("eps", 0),
            "margin_ratio": 0,
            "institutional_data": inst_data,
            "ai_prediction": "分析中...",
            "news": "無新聞"
        }
        time.sleep(2)

    # 原子寫入邏輯：防止 JSON 檔案損壞
    temp_file = "market_data.json.tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    
    # 直接取代舊檔案
    os.replace(temp_file, "market_data.json")
    print("檔案已安全更新。")

if __name__ == "__main__":
    run_main()
