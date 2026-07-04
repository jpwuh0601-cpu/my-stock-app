import yfinance as yf
import json
import os
import random
import datetime

# 確保寫入結構始終一致
def run_analysis_and_update():
    target_file = "market_data.json"
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW"]
    data = {}
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 強制定義結構，確保所有 Key 都存在，避免前端 AttributeError
            data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "change": 0,
                "nav": info.get("bookValue") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "margin_ratio": 0,
                "institutional_data": [{"日期": "N/A", "外資": 0, "投信": 0, "自營商": 0}],
                "ai_prediction": "分析數據初始化中...",
                "news": "最新市場動態待更新。",
                "black_swan": "安全"
            }
        except Exception as e:
            print(f"[-] 抓取失敗 {symbol}: {e}")
            
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
