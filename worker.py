import sys
import os
import json
import time
import yfinance as yf

# 【關鍵修正】確保系統能找到同目錄下的 analyzer.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from analyzer import get_ai_analysis
except ImportError as e:
    print(f"致命錯誤：無法匯入 analyzer 模組。請確認 analyzer.py 是否存在於 {current_dir}")
    raise e

def run_analysis_and_update():
    # ... (其餘程式碼保持不變)
    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    market_data = {}
    for ticker_symbol in tickers:
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            data = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "ai_prediction": get_ai_analysis(ticker_symbol)
            }
            market_data[ticker_symbol] = data
            time.sleep(2) 
        except Exception as e:
            print(f"分析失敗: {e}")
            
    with open(os.path.join(current_dir, "market_data.json"), "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)
