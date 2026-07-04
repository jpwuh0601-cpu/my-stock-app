import json
import time
import yfinance as yf
from analyzer import get_ai_analysis

def run_analysis_and_update():
    # 讀取標的清單
    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    market_data = {}
    
    for ticker_symbol in tickers:
        try:
            print(f"正在分析: {ticker_symbol}...")
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            # 獲取基礎數據
            data = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "ai_prediction": get_ai_analysis(ticker_symbol)
            }
            market_data[ticker_symbol] = data
            
            # 重要：強行暫停，防止觸發 Yahoo 限制
            time.sleep(3) 
            
        except Exception as e:
            print(f"分析 {ticker_symbol} 失敗: {e}")
            
    # 寫入結果
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)
    print("數據更新完畢。")

if __name__ == "__main__":
    run_analysis_and_update()
