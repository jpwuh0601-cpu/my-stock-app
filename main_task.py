import json
import os
from worker import fetch_stock_data, fetch_real_broker_data

def main():
    final_data = {}
    
    # 1. 讀取 tickers.txt 確保正確讀取股票清單
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r", encoding="utf-8") as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        tickers = ["2330.TW", "2317.TW", "2454.TW"]

    print(f"DEBUG: 開始執行分析，目標股票: {tickers}")

    # 2. 執行爬蟲與分析邏輯
    for ticker in tickers:
        try:
            print(f"DEBUG: 正在處理: {ticker}")
            
            # 獲取各項數據
            stock_info = fetch_stock_data(ticker)
            broker_info = fetch_real_broker_data(ticker)
            
            # 檢查數據是否有抓到 (若為 None 或空列表則發出警告)
            if not stock_info and not broker_info:
                print(f"警告: 無法獲取 {ticker} 的有效資料")
                continue
            
            # 將數據存入字典
            final_data[ticker] = {
                "price": stock_info.get("price", 0) if isinstance(stock_info, dict) else 0,
                "ai_report": f"券商分析: {broker_info[:3] if broker_info else '無資料'}",
                "raw_info": stock_info
            }
            print(f"DEBUG: {ticker} 資料已載入，目前資料筆數: {len(final_data)}")
            
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 時發生錯誤: {e}")

    # 3. 強制寫入檔案
    if final_data:
        try:
            with open("market_data.json", "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=4)
            print("SUCCESS: 數據已寫入 market_data.json")
        except Exception as e:
            print(f"ERROR: 寫入檔案失敗: {e}")
    else:
        print("ERROR: 未產生任何有效數據，請檢查 worker.py 的爬蟲函數是否正常運作。")

if __name__ == "__main__":
    main()
