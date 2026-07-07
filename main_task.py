import json
import os
import sys
import time
import requests
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def fetch_hot_tickers():
    """自動從 Yahoo Finance 熱門頁面獲取部分台股熱門代號"""
    # 這裡作為示範，使用預設熱門清單。
    # 進階可透過 requests 爬取 Yahoo Finance 熱門排行榜頁面
    print("📈 正在自動獲取市場熱門股票代號...")
    return ["2330.TW", "2317.TW", "2454.TW", "2303.TW", "0050.TW"]

def run_main(target_tickers=None):
    """執行股市數據抓取與AI分析"""
    
    # 若無傳入參數，則自動獲取熱門代號
    if not target_tickers:
        target_tickers = fetch_hot_tickers()

    final_results = {}
    print(f"🚀 開始資料更新，目標股票: {target_tickers}")

    for ticker in target_tickers:
        print(f"🔍 正在獲取 {ticker} 的完整數據...")
        
        # 抓取資料
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        
        info = stock_info.get("info", {})
        ai_result = generate_ai_analysis(ticker, str(info), str(inst_data))
        
        final_results[ticker] = {
            "price": stock_info.get("price") or info.get("currentPrice") or 0.0,
            "nav": info.get("bookValue") or 0.0,
            "pe": info.get("trailingPE") or 0.0,
            "eps": info.get("trailingEps") or 0.0,
            "ai_prediction": ai_result.get("main_force_analysis", "AI 正在分析中..."),
            "institutional_data": inst_data if inst_data else "無法人籌碼資料"
        }
        
        time.sleep(6)

    # 寫入檔案
    output_path = os.path.join(os.getcwd(), "market_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("✅ 成功更新資料。")

if __name__ == "__main__":
    # 支援指令列參數覆蓋自動抓取的名單
    args = sys.argv[1:]
    run_main(target_tickers=args if args else None)
