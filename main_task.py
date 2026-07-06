import json
import os
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    # 讀取股票代號清單
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    for ticker in tickers:
        try:
            print(f"正在抓取: {ticker}")
            stock = fetch_stock_data(ticker)
            inst = fetch_institutional_data(ticker)
            
            # 將 8 項數據結構化，轉為字串以防渲染錯誤
            final_results[ticker] = {
                "price": str(stock.get("price", "0")),
                "eps": str(stock.get("eps", "0")),
                "nav": "0",  # 預留位
                "pe": "0",   # 預留位
                "institutional_data": inst if isinstance(inst, list) else [],
                "ai_prediction": "AI 財報預測分析中...",
                "news": "無最新即時新聞",
                "annual_forecast": "營收與股利預估分析中..."
            }
        except Exception as e:
            print(f"抓取 {ticker} 錯誤: {e}")

    # 寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("數據已寫入 market_data.json")

if __name__ == "__main__":
    run_main()
