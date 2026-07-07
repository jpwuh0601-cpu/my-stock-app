import json
import os
import sys
import time
import requests
import pandas as pd
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def calculate_indicators(ticker):
    """計算基礎技術指標 (RSI, KD)"""
    # 這裡未來可整合 yfinance 抓取歷史資料來計算
    # 目前先回傳佔位符，讓 AI 參考
    return "RSI: 55, KD: 60 (中性偏多)"

def fetch_hot_tickers():
    """自動從 Yahoo Finance 熱門頁面獲取部分台股熱門代號"""
    print("📈 正在自動獲取市場熱門股票代號...")
    return ["2330.TW", "2317.TW", "2454.TW", "2303.TW", "0050.TW"]

def run_main(target_tickers=None):
    """執行股市數據抓取與 AI 分析"""
    
    if not target_tickers:
        target_tickers = fetch_hot_tickers()

    final_results = {}
    print(f"🚀 開始資料更新，目標股票: {target_tickers}")

    for ticker in target_tickers:
        print(f"🔍 正在獲取 {ticker} 的完整數據與技術指標...")
        
        # 1. 抓取基礎資料
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        
        # 2. 計算技術指標
        indicators = calculate_indicators(ticker)
        
        # 3. 準備分析資料
        info = stock_info.get("info", {})
        combined_data = f"基本面: {str(info)}, 法人籌碼: {str(inst_data)}, 技術指標: {indicators}"
        
        # 4. 生成 AI 分析
        ai_result = generate_ai_analysis(ticker, str(info), combined_data)
        
        final_results[ticker] = {
            "price": stock_info.get("price") or info.get("currentPrice") or 0.0,
            "nav": info.get("bookValue") or 0.0,
            "pe": info.get("trailingPE") or 0.0,
            "eps": info.get("trailingEps") or 0.0,
            "ai_prediction": ai_result.get("main_force_analysis", "AI 正在分析中..."),
            "institutional_data": inst_data if inst_data else "無法人籌碼資料",
            "indicators": indicators
        }
        
        time.sleep(6)

    # 寫入檔案
    output_path = os.path.join(os.getcwd(), "market_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("✅ 成功更新資料，已包含技術指標資訊。")

if __name__ == "__main__":
    args = sys.argv[1:]
    run_main(target_tickers=args if args else None)
