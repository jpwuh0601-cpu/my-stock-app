import json
import time
import os
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    """
    主任務腳本：負責抓取資料並寫入 market_data.json
    """
    # 讀取目標股票清單
    ticker_file = "tickers.txt"
    if os.path.exists(ticker_file):
        with open(ticker_file, "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

    final_results = {}
    print(f"DEBUG: 開始執行任務，處理目標: {tickers}")

    for ticker in tickers:
        try:
            print(f"DEBUG: 正在處理 {ticker}...")
            # 抓取股價與基本面
            stock_data = fetch_stock_data(ticker)
            # 抓取籌碼面
            inst_data = fetch_institutional_data(ticker)
            
            # 將資料標準化，確保即使缺失也不會寫入 None 或非法結構
            # 這裡統一轉為字串，方便 app.py 的 Streamlit 表格渲染
            final_results[ticker] = {
                "price": str(stock_data.get("price", "0")),
                "eps": str(stock_data.get("eps", "0")),
                "nav": "0",  # 預留位，可由 worker.py 擴充
                "pe": "0",   # 預留位，可由 worker.py 擴充
                "institutional_data": inst_data if isinstance(inst_data, list) else [],
                "ai_prediction": "AI 正在分析中...",
                "news": "目前無最新即時新聞"
            }
            # 避免觸發 Yahoo Finance 防爬蟲機制
            time.sleep(5) 
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 時發生錯誤: {e}")

    # 安全寫入 JSON，確保檔案結構為 UTF-8
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("DEBUG: market_data.json 已成功寫入。")
    except Exception as e:
        print(f"DEBUG: 檔案寫入失敗: {e}")

if __name__ == "__main__":
    run_main()
