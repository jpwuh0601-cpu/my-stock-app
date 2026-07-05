import json
import os
# 假設您引用了 worker.py 中的爬蟲函數
from worker import fetch_stock_data

def main():
    final_data = {}
    
    # 讀取 tickers.txt 確保股票清單正確
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        tickers = ["2330.TW", "2317.TW", "2454.TW"]

    print(f"開始分析股票: {tickers}")

    for ticker in tickers:
        try:
            # 這裡呼叫您的爬蟲函數，請確保 fetch_stock_data 有正確回傳資料
            data = fetch_stock_data(ticker)
            
            # 確保資料不為空才寫入
            if data:
                final_data[ticker] = data
                print(f"成功處理: {ticker}")
            else:
                print(f"警告: 無法獲取 {ticker} 的數據")
        except Exception as e:
            print(f"處理 {ticker} 時發生錯誤: {e}")

    # 強制寫入邏輯
    if final_data:
        try:
            with open("market_data.json", "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=4)
            print("數據成功寫入 market_data.json")
        except Exception as e:
            print(f"寫入檔案失敗: {e}")
    else:
        print("警告：未收集到任何數據，為避免覆蓋，跳過寫入。")

if __name__ == "__main__":
    main()
