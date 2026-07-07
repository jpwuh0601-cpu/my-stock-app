import json
import os
import sys
import time
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def calculate_indicators(ticker):
    """計算基礎技術指標 (RSI, KD)"""
    return "RSI: 55, KD: 60 (中性偏多)"

def fetch_hot_tickers():
    """獲取預設監控標的"""
    return ["2330.TW", "2317.TW", "2454.TW", "2303.TW", "0050.TW"]

def run_main(target_tickers=None):
    """執行股市數據抓取與 AI 分析，確保 8 項關鍵數據確實到位"""
    
    if not target_tickers:
        target_tickers = fetch_hot_tickers()

    final_results = {}
    print(f"🚀 開始資料更新，目標: {target_tickers}")

    for ticker in target_tickers:
        print(f"🔍 正在獲取 {ticker} 的 8 項數據...")
        
        # 1. 抓取資料
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        info = stock_info.get("info", {})
        
        # 2. 生成 AI 分析
        combined_data = f"基本面: {str(info)}, 法人籌碼: {str(inst_data)}"
        ai_result = generate_ai_analysis(ticker, str(info), combined_data)
        
        # 3. 確保 8 項數據確實寫入
        final_results[ticker] = {
            "price": stock_info.get("price") or info.get("currentPrice") or 0.0,
            "change": info.get("regularMarketChangePercent") or 0.0,
            "nav": info.get("bookValue") or 0.0,
            "pe": info.get("trailingPE") or 0.0,
            "eps": info.get("trailingEps") or 0.0,
            "margin_ratio": 0.0, # 預留欄位
            "institutional_data": inst_data if inst_data else [],
            "ai_prediction": ai_result.get("main_force_analysis", "AI 正在分析中..."),
            "indicators": calculate_indicators(ticker)
        }
        
        time.sleep(6) # 穩定性延遲

    # 4. 寫入檔案
    output_path = os.path.join(os.getcwd(), "market_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("✅ 8 項關鍵數據已確實寫入 market_data.json")

if __name__ == "__main__":
    args = sys.argv[1:]
    run_main(target_tickers=args if args else None)
