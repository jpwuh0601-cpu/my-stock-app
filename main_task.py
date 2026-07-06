import json
import os
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis

def get_tickers():
    # 從 tickers.txt 讀取
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    return ["2330.TW"]

def main():
    tickers = get_tickers()
    final_results = {}

    for ticker in tickers:
        try:
            print(f"正在分析: {ticker}...")
            stock_info = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            broker_data = fetch_top_brokers_data(ticker)
            
            ai_result = generate_ai_analysis(ticker, stock_info.get("info", {}), broker_data.to_dict('records') if hasattr(broker_data, 'to_dict') else [])
            
            final_results[ticker] = {
                "price": stock_info.get("price", 0),
                "institutional_data": inst_data if inst_data else [],
                "ai_prediction": ai_result.get("main_force_analysis", "分析暫時無法取得")
            }
        except Exception as e:
            print(f"分析 {ticker} 時發生錯誤: {e}")
            continue # 確保其中一檔股票失敗時，不會中斷整個程式

    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("SUCCESS: JSON 更新完成")

if __name__ == "__main__":
    main()
