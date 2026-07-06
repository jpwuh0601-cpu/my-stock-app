import json
import os
import sys

# 1. 強制加入當前目錄至系統路徑，解決 ModuleNotFoundError
sys.path.append(os.getcwd())

from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis

def get_tickers():
    """從 tickers.txt 讀取股票代號清單"""
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["2330.TW"] # 預設值

def main():
    tickers = get_tickers()
    final_results = {}
    
    print(f"開始分析，共計 {len(tickers)} 檔股票...")

    for ticker in tickers:
        try:
            print(f"正在處理: {ticker}...")
            
            # 取得各項數據
            stock_info = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            broker_data = fetch_top_brokers_data(ticker)
            
            # 確保 broker_data 是可用的格式
            broker_records = broker_data.to_dict('records') if hasattr(broker_data, 'to_dict') else []
            
            # 進行 AI 分析
            ai_result = generate_ai_analysis(ticker, stock_info.get("info", {}), broker_records)
            
            # 組合結果
            final_results[ticker] = {
                "price": stock_info.get("price", 0),
                "institutional_data": inst_data if inst_data else [{"日期": "無資料", "外資": 0, "投信": 0, "自營商": 0}],
                "ai_prediction": ai_result.get("main_force_analysis", "分析服務暫時中斷"),
                "last_update": "2026-07-06"
            }
            
        except Exception as e:
            print(f"處理 {ticker} 時發生不可預期的錯誤: {e}")
            # 即使失敗，也保留一個基本結構以防網頁崩潰
            final_results[ticker] = {
                "price": 0,
                "institutional_data": [],
                "ai_prediction": "資料抓取失敗"
            }
            continue 

    # 將結果寫入檔案，確保格式正確
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("SUCCESS: 檔案已成功更新至 market_data.json")
    except Exception as e:
        print(f"寫入檔案失敗: {e}")

if __name__ == "__main__":
    main()
