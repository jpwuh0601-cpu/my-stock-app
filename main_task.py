import json
import time
import os
from worker import (
    fetch_stock_data, 
    fetch_institutional_data, 
    fetch_top_brokers_data, 
    check_black_swan
)
from analyzer import check_geopolitical_risk

def run_main():
    # 讀取目標股票代號清單
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file):
        print(f"找不到 {ticker_file}，請確保該檔案存在")
        return

    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    final_results = {}

    # 1. 先執行一次全局地緣政治風險分析 (避免重複呼叫 API)
    geo_status, geo_reasons = check_geopolitical_risk()
    print(f"地緣政治風險評估完成: {geo_status}")

    # 2. 逐一處理每檔股票
    for ticker in tickers:
        print(f"正在處理: {ticker} ...")
        try:
            # 獲取股價與財報資訊
            stock_data = fetch_stock_data(ticker)
            
            if "error" in stock_data:
                print(f"獲取 {ticker} 資料失敗: {stock_data['error']}")
                continue
            
            # 獲取財務狀態
            info = stock_data.get("info", {})
            black_swan_status, black_swan_reasons = check_black_swan(info)
            
            # 整合所有資料
            final_results[ticker] = {
                "price": stock_data.get("price", 0),
                "institutional_data": fetch_institutional_data(ticker),
                "broker_data_snippet": "已更新", # 簡化寫入以防檔案過大
                "black_swan_company": black_swan_status,
                "black_swan_global": geo_status,
                "black_swan_global_reasons": geo_reasons,
                "last_update": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 關鍵防護：強制延遲，避免 Yahoo Finance 封鎖
            time.sleep(8) 
            
        except Exception as e:
            print(f"處理 {ticker} 時發生未知錯誤: {e}")

    # 3. 將最終結果寫入 JSON 檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    
    print("所有資料更新完成，已寫入 market_data.json")

if __name__ == "__main__":
    run_main()
