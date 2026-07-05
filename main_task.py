import json
import os
import yfinance as yf
from worker import fetch_stock_data, fetch_real_broker_data

def main():
    final_data = {}
    tickers = ["2330.TW", "2317.TW", "2454.TW"]
    
    print(f"DEBUG: 啟動分析，目標清單: {tickers}")

    for ticker in tickers:
        print(f"DEBUG: 正在處理 {ticker}")
        
        # 獲取資料
        stock_info = fetch_stock_data(ticker)
        broker_info = fetch_real_broker_data(ticker)
        
        # 診斷：檢查 yfinance 是否回傳空值
        if not stock_info or stock_info.get("price") == 0:
            print(f"DEBUG: 警告！{ticker} 的 yfinance 抓取為空，嘗試強制重新建立物件...")
            try:
                t = yf.Ticker(ticker)
                print(f"DEBUG: Ticker info 測試: {t.info.get('currentPrice')}")
            except Exception as e:
                print(f"DEBUG: 致命錯誤: {e}")

        final_data[ticker] = {
            "price": stock_info.get("price", 0),
            "ai_report": f"券商分析: {broker_info[0].get('券商', '無資料')}" if broker_info else "無資料",
            "raw_info": stock_info
        }

    # 強制寫入
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print("SUCCESS: 數據已寫入 market_data.json")
    except Exception as e:
        print(f"ERROR: 寫入失敗: {e}")

if __name__ == "__main__":
    main()
