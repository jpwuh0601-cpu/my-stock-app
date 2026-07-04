import yfinance as yf
import json
import os
import random
import datetime

# 定義檔案路徑
TICKERS_FILE = "tickers.txt"
DATA_FILE = "market_data.json"

def get_target_tickers():
    """讀取 tickers.txt，若檔案不存在則返回預設列表"""
    if os.path.exists(TICKERS_FILE):
        with open(TICKERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

def get_mock_institutional_data():
    """生成 10 日法人買賣超模擬數據"""
    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d") for i in range(10)]
    return [
        {"日期": d, "外資": random.randint(-5000, 5000), "投信": random.randint(-1000, 1000), "自營商": random.randint(-2000, 2000)}
        for d in dates
    ]

def run_analysis_and_update():
    """主執行邏輯：抓取資料並寫入 JSON"""
    tickers = get_target_tickers()
    data = {}
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 使用 get 提供預設值，防止 AttributeError
            data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "change": round(random.uniform(-5, 5), 2),
                "nav": info.get("bookValue") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "margin_ratio": round(random.uniform(1, 15), 2),
                "institutional_data": get_mock_institutional_data(),
                "news": "市場動態：總體經濟溫和成長中。",
                "ai_prediction": f"{symbol} AI 趨勢預測：籌碼面維持穩健，建議持續觀察量能變化。",
                "black_swan": "安全",
                "main_force": "法人加碼",
                "foreign_analysis": "看好",
                "gpt_insight": "AI 綜合洞察：技術線型呈現多頭排列。"
            }
        except Exception as e:
            print(f"[-] 抓取失敗 {symbol}: {e}")
            
    # 安全寫入檔案
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[+] 資料已更新至 {DATA_FILE}")
    except Exception as e:
        print(f"[-] 寫入檔案失敗: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
