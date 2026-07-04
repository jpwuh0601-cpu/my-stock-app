import yfinance as yf
import json
import os
import random
import datetime

# 定義監控標的檔案路徑
TICKERS_FILE = "tickers.txt"

def get_target_tickers():
    """從 tickers.txt 讀取代號，若無則使用預設清單"""
    if os.path.exists(TICKERS_FILE):
        with open(TICKERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

def get_mock_institutional_data():
    """模擬三大法人與券商資料，未來可串接 twstock API"""
    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d") for i in range(10)]
    return [
        {"日期": d, "外資": random.randint(-5000, 5000), "投信": random.randint(-1000, 1000), "自營商": random.randint(-2000, 2000)}
        for d in dates
    ]

def run_analysis_and_update():
    target_file = "market_data.json"
    tickers = get_target_tickers()
    data = {}
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 整理資料結構以符合前端要求
            data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "change": round(random.uniform(-10, 10), 2), # 模擬漲跌幅
                "nav": info.get("bookValue", 0),
                "pe": info.get("forwardPE", 0),
                "eps": info.get("trailingEps", 0),
                "margin_ratio": round(random.uniform(5, 20), 2),
                "institutional_data": get_mock_institutional_data(),
                "ai_prediction": f"{symbol} AI 綜合評估：近期法人籌碼呈現中性，建議持續觀察。",
                "news": "最新市場動態：總體經濟數據顯示通膨壓力減緩。",
                "black_swan": "無異常"
            }
        except Exception as e:
            print(f"[-] 抓取失敗 {symbol}: {e}")
            
    # 寫入 JSON
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[+] 數據已成功更新至 {target_file}")

if __name__ == "__main__":
    run_analysis_and_update()
