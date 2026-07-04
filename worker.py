import sys
import os
import json
import time
import yfinance as yf

# 強制將當前腳本所在目錄設定為最高優先搜尋路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    import analyzer
except ImportError:
    # 如果真的找不到，直接報錯提示明確路徑
    raise ImportError(f"無法在 {BASE_DIR} 目錄下找到 analyzer.py，請確認檔案已上傳至 GitHub 根目錄。")

def run_analysis_and_update():
    with open(os.path.join(BASE_DIR, "tickers.txt"), "r") as f:
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
                "ai_prediction": analyzer.get_ai_analysis(ticker_symbol)
            }
            market_data[ticker_symbol] = data
            time.sleep(2)
        except Exception as e:
            print(f"分析 {ticker_symbol} 失敗: {e}")
            
    with open(os.path.join(BASE_DIR, "market_data.json"), "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
