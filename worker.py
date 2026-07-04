import yfinance as yf
import requests
import json
import os
import twstock # 已包含在 requirements.txt 中

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_chip_data(symbol):
    """使用 twstock 獲取籌碼與資券比"""
    code = symbol.replace('.TW', '')
    try:
        # 獲取三大法人買賣超資訊
        # 注意：twstock 獲取籌碼面需連接證交所 API
        data = twstock.Realtime(code).get()
        
        # 模擬法人資料：實務上可透過 twstock 歷史資料庫計算 10 日平均
        return {
            "資券比": 15.2, # 範例數據，之後可替換為計算值
            "法人買賣超": 1250 # 範例數據
        }
    except:
        return {"資券比": 0, "法人買賣超": 0}

def run_analysis_and_update():
    default_tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    data = {}
    
    for symbol in default_tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            chip = get_chip_data(symbol)
            
            data[symbol] = {
                "price": info.get("currentPrice", 0),
                "change": round(info.get("regularMarketChangePercent", 0), 2),
                "eps": info.get("trailingEps", 0),
                "chip_data": chip,
                "black_swan": "⚠️ 高風險" if info.get("regularMarketChangePercent", 0) <= -3 else "安全"
            }
        except Exception as e:
            print(f"Error {symbol}: {e}")
            
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
