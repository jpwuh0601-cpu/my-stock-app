import json
import time
import os
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    # 8 項指標的目標股票清單
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    for ticker in tickers:
        print(f"正在抓取 {ticker} 的 8 項數據...")
        try:
            # 獲取基礎數據
            stock = fetch_stock_data(ticker)
            inst = fetch_institutional_data(ticker)
            
            # 將 8 項數據結構化寫入
            final_results[ticker] = {
                "price": str(stock.get("price", "0")),          # 1. 即時股價
                "nav": str(stock.get("nav", "0")),               # 2. 每股淨額
                "pe": str(stock.get("pe", "0")),                 # 3. 本益比
                "eps": str(stock.get("eps", "0")),               # 4. 每股盈餘
                "quarterly_report": "等待季度資料源",             # 5. 每季報表
                "institutional_data": inst if isinstance(inst, list) else [], # 6. 三大法人
                "margin_trading": "等待資券比資料",               # 7. 資券比與主力
                "news": "無最新新聞",                            # 8. 即時新聞
                "ai_prediction": "AI 分析生成中..."               # 額外補充
            }
            time.sleep(3) # 避免 API 超頻
        except Exception as e:
            print(f"處理 {ticker} 發生錯誤: {e}")

    # 寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("所有數據已成功寫入 market_data.json")

if __name__ == "__main__":
    run_main()
