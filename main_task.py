import json
import os
from worker import fetch_stock_data, fetch_real_broker_data

def main():
    final_data = {}
    tickers = ["2330.TW", "2317.TW", "2454.TW"]
    
    print(f"DEBUG: 開始執行，目標股票: {tickers}")

    for ticker in tickers:
        try:
            # 分別獲取兩部分資料
            stock_info = fetch_stock_data(ticker)
            broker_info = fetch_real_broker_data(ticker)
            
            # 偵錯用：將抓到的資料直接印出來
            print(f"DEBUG: {ticker} 爬取結果 -> Stock: {stock_info}, Broker: {broker_info}")
            
            # 將數據存入字典
            final_data[ticker] = {
                "price": stock_info.get("price", 0),
                "ai_report": f"券商分析: {broker_info[0].get('券商', '無資料')}" if broker_info else "無資料",
                "raw_info": stock_info
            }
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 發生錯誤: {e}")

    # 強制將結果寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        print("SUCCESS: 數據已寫入 market_data.json")

if __name__ == "__main__":
    main()
