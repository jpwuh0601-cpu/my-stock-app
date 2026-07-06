import json
import os
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis

def get_tickers():
    """從設定檔讀取需要分析的股票列表"""
    try:
        with open("tickers.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["2330.TW"]

def main():
    tickers = get_tickers()
    final_results = {}

    for ticker in tickers:
        print(f"正在分析: {ticker}...")
        try:
            # 1. 取得真實市場數據
            stock_info = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            broker_data = fetch_top_brokers_data(ticker)
            
            # 檢查是否讀取失敗
            if "error" in stock_info:
                print(f"跳過 {ticker}: {stock_info['error']}")
                continue

            # 2. 呼叫 AI 深度分析 (串接 analyzer.py)
            ai_result = generate_ai_analysis(
                ticker, 
                stock_info.get("info", {}), 
                broker_data.to_dict('records')
            )
            
            # 3. 整合最終數據結構
            final_results[ticker] = {
                "price": stock_info.get("price", 0),
                "eps": stock_info.get("eps", 0),
                "institutional_data": inst_data.to_dict(orient='records'),
                "ai_prediction": ai_result.get("main_force_analysis", "分析失敗"),
                "last_update": "2026-07-06"
            }
            
        except Exception as e:
            print(f"分析 {ticker} 時發生錯誤: {e}")

    # 4. 寫入 market_data.json
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("SUCCESS: 所有資料已更新至 market_data.json")
    except Exception as e:
        print(f"寫入檔案失敗: {e}")

if __name__ == "__main__":
    main()
