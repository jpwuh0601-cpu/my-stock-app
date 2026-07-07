import json
import time
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    for ticker in tickers:
        stock_info = fetch_stock_data(ticker)
        
        # 建立平鋪結構，避免 JSON 層級過深
        final_results[ticker] = {
            "price": stock_info.get("price", 0),
            "eps": stock_info.get("eps", 0),
            "nav": stock_info.get("info", {}).get("bookValue", 0),
            "pe": stock_info.get("info", {}).get("trailingPE", 0),
            "ai_report": "AI 分析分析中...", 
            "institutional_data": fetch_institutional_data(ticker)
        }
        time.sleep(5) # 遵守 API 速率限制

    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_main()
