import yfinance as yf
import requests
import json
import os
import datetime
import twstock

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_chip_data(symbol):
    """使用 twstock 獲取籌碼與資券比"""
    code = symbol.replace('.TW', '')
    stock = twstock.Stock(code)
    # 獲取最近的資券與法人數據 (twstock 的 fetch 接口)
    # 注意：需確保網路環境可訪問證交所數據
    try:
        # 這裡簡易示範獲取資料結構
        return {"資券比": 12.5, "法人買賣超": 500} 
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
                "pe": info.get("forwardPE", 0),
                "chip_data": chip,
                "black_swan": "⚠️ 高風險" if info.get("regularMarketChangePercent", 0) <= -3 else "安全"
            }
        except Exception as e:
            print(f"Error {symbol}: {e}")
            
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
