import json
import time
import os
import yfinance as yf
import requests

# 這裡直接將原本 analyzer.py 的功能內嵌，不再需要 import
def get_ai_analysis_direct(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    news = ticker.news
    latest_news = news[0]['title'] if news else "目前無最新新聞報導"
    
    prompt = f"針對 {ticker_symbol} 進行財報分析，EPS: {info.get('trailingEps', 'N/A')}，PE: {info.get('forwardPE', 'N/A')}。新聞: {latest_news}。"
    
    if not api_key:
        return f"新聞: {latest_news}"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except:
        return "AI 分析暫時無法取得。"

def run_analysis_and_update():
    # 使用絕對路徑確保讀取正確
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tickers_path = os.path.join(base_dir, "tickers.txt")
    
    with open(tickers_path, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    market_data = {}
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            market_data[symbol] = {
                "price": info.get("currentPrice") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "ai_prediction": get_ai_analysis_direct(symbol),
                "black_swan": "安全"
            }
            time.sleep(2)
        except Exception as e:
            print(f"處理 {symbol} 時發生錯誤: {e}")
            
    with open(os.path.join(base_dir, "market_data.json"), "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
