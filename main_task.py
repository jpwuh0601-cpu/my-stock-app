import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    # 測試用清單，確保至少有一檔股票能抓到
    tickers = ["2330.TW"] 
    final_results = {}

    for ticker in tickers:
        try:
            print(f"DEBUG: 正在抓取 {ticker}")
            stock_info = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            
            # 強制檢查是否有資料
            price = stock_info.get("price", 0)
            if price == 0:
                print(f"DEBUG: {ticker} 抓到價格為 0")
            
            final_results[ticker] = {
                "price": price,
                "nav": 0, "pe": 0, "eps": stock_info.get("eps", 0),
                "institutional_data": inst_data,
                "ai_prediction": "測試中",
                "news": "測試中"
            }
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 時發生錯誤: {e}")

    # 寫入檔案
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("DEBUG: 檔案寫入成功")
    except Exception as e:
        print(f"DEBUG: 檔案寫入失敗: {e}")

if __name__ == "__main__":
    run_main()
