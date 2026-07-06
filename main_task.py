import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    # 讀取 tickers.txt
    try:
        with open("tickers.txt", "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
    except:
        tickers = ["2330.TW", "2317.TW", "2454.TW"]

    final_results = {}
    print(f"DEBUG: 開始執行，處理清單: {tickers}")

    for ticker in tickers:
        try:
            print(f"DEBUG: 正在處理 {ticker}...")
            stock_data = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            
            # 使用 .get() 確保即使數據缺失也不會崩潰
            final_results[ticker] = {
                "price": stock_data.get("price", 0),
                "eps": stock_data.get("eps", 0),
                "institutional_data": inst_data if inst_data else [],
                "ai_prediction": "分析完成",
                "news": "無最新新聞"
            }
            time.sleep(5) # 降低頻率避免被封鎖
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 失敗: {e}")

    # 寫入檔案
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("DEBUG: 檔案寫入成功。")
    except Exception as e:
        print(f"DEBUG: 寫入檔案失敗: {e}")

if __name__ == "__main__":
    run_main()
