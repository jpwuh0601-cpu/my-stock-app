import json
import time
import os
import yfinance as yf
import requests

def get_ai_analysis(ticker_symbol):
    """直接在 worker 內部處理 AI 分析邏輯"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "未設定 API Key，無法取得 AI 分析。"

    ticker = yf.Ticker(ticker_symbol)
    try:
        info = ticker.info
        news = ticker.news
        latest_news = news[0]['title'] if news else "目前無最新新聞報導"
        
        prompt = f"針對 {ticker_symbol} 進行財報分析。EPS: {info.get('trailingEps', 'N/A')}，PE: {info.get('forwardPE', 'N/A')}。最新新聞: {latest_news}。請簡單給予投資觀點。"
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析發生錯誤: {str(e)}"

def run_analysis_and_update():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tickers_path = os.path.join(base_dir, "tickers.txt")
    
    if not os.path.exists(tickers_path):
        print("錯誤：找不到 tickers.txt")
        return

    with open(tickers_path, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    market_data = {}
    for symbol in tickers:
        try:
            print(f"正在分析: {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            market_data[symbol] = {
                "price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
                "pe": info.get("forwardPE") or 0,
                "eps": info.get("trailingEps") or 0,
                "ai_prediction": get_ai_analysis(symbol),
                "black_swan": "安全"
            }
            time.sleep(2)
        except Exception as e:
            print(f"處理 {symbol} 時發生錯誤: {e}")
            
    with open(os.path.join(base_dir, "market_data.json"), "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)
    print("數據更新完畢。")

if __name__ == "__main__":
    run_analysis_and_update()
