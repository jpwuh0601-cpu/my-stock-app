import json
import os
import sys
import time
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def run_main(target_tickers=None):
    """執行股市數據抓取與AI分析，支援動態傳入股票代號"""
    
    # 若無傳入參數，則嘗試讀取 tickers.txt，否則使用傳入的列表
    if not target_tickers:
        try:
            with open("tickers.txt", "r", encoding="utf-8") as f:
                target_tickers = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("❌ 錯誤: 未提供代號且找不到 tickers.txt")
            return

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
    # 允許透過指令執行: python main_task.py 2330.TW 2454.TW
    args = sys.argv[1:]
    run_main(target_tickers=args if args else None)
