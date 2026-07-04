import json
import time
import os
import yfinance as yf
import requests

def get_ai_analysis(ticker_symbol):
    """直接在函數內部處理分析，無需 import 其他檔案"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    try:
        info = ticker.info
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        prompt = f"針對 {ticker_symbol} 進行財報分析。EPS: {info.get('trailingEps', 'N/A')}，PE: {info.get('forwardPE', 'N/A')}。新聞: {latest_news}。"
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "google/gemini-2.0-flash-exp:free", "messages": [{"role": "user", "content": prompt}]}
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"分析失敗: {e}"

def run_analysis_and_update():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tickers_file = os.path.join(base_dir, "tickers.txt")
    output_file = os.path.join(base_dir, "market_data.json")
    
    with open(tickers_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
        
    market_data = {}
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        market_data[symbol] = {
            "price": info.get("currentPrice") or 0,
            "pe": info.get("forwardPE") or 0,
            "eps": info.get("trailingEps") or 0,
            "ai_prediction": get_ai_analysis(symbol),
            "black_swan": "安全"
        }
        time.sleep(2)
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
