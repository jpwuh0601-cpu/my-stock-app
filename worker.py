import yfinance as yf
import json
import os
import random
import datetime

# 定義檔案路徑
TICKERS_FILE = "tickers.txt"
DATA_FILE = "market_data.json"

def get_target_tickers():
    if os.path.exists(TICKERS_FILE):
        with open(TICKERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

def run_analysis_and_update():
    tickers = get_target_tickers()
    data = {}
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "change": round(random.uniform(-5, 5), 2),
                "nav": info.get("bookValue") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "margin_ratio": round(random.uniform(1, 15), 2),
                "institutional_data": [{"日期": "07-04", "外資": 0, "投信": 0, "自營商": 0}],
                "news": "最新市場動態成長中。",
                "ai_prediction": "AI 分析中...",
                "black_swan": "安全",
                "main_force": "主力加碼",
                "foreign_analysis": "外資持平",
                "gpt_insight": "趨勢看多",
                "ai_selection": "推薦關注"
            }
        except Exception as e:
            print(f"[-] 抓取 {symbol} 失敗: {e}")
            
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
