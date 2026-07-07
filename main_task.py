import json
import os
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    for ticker in tickers:
        stock_info = fetch_stock_data(ticker)
        # 直接儲存為平鋪結構，或者對齊您之前的 raw_info 結構
        final_results[ticker] = {
            "price": stock_info.get("price", 0),
            "ai_report": "AI 正在分析中...",
            "raw_info": stock_info # 包含完整 info 資料
        }

    # 確保寫入根目錄
    output_path = os.path.join(os.getcwd(), "market_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print(f"資料已寫入至: {output_path}")

if __name__ == "__main__":
    run_main()
