import json
import os
from worker import fetch_stock_data, fetch_real_broker_data

def main():
    final_data = {}
    
    # 讀取 tickers.txt
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r", encoding="utf-8") as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        tickers = ["2330.TW", "2317.TW", "2454.TW"]

    print(f"DEBUG: 開始執行，目標股票: {tickers}")

    for ticker in tickers:
        try:
            print(f"DEBUG: 正在處理 {ticker}")
            stock_info = fetch_stock_data(ticker)
            broker_info = fetch_real_broker_data(ticker)
            
            # 整合數據
            final_data[ticker] = {
                "price": stock_info.get("price", 0),
                "ai_report": f"券商分析: {broker_info[0]['券商'] if broker_info else '無資料'}",
                "raw_info": stock_info
            }
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 發生錯誤: {e}")

    # 強制將結果寫入檔案
    if final_data:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print("SUCCESS: 數據已寫入 market_data.json")
    else:
        print("ERROR: 未取得任何數據，跳過寫入。")

if __name__ == "__main__":
    main()
