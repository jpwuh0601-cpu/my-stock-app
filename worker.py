import yfinance as yf
import requests
import json
import os

# 從環境變數讀取 OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_sentiment(news_title):
    """呼叫 OpenRouter AI 進行新聞情緒分析"""
    if not OPENROUTER_API_KEY:
        return "AI 分析未啟用 (缺少 API Key)"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{news_title}。請用一句話簡短總結市場觀點。"}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception:
        return "分析暫時中斷"

def run_analysis_and_update():
    # ... (原有抓取邏輯)
    ticker = yf.Ticker(symbol)
    news = ticker.news
    latest_news = news[0]['title'] if news else "無最新新聞"
    
    # 進行 AI 分析
    ai_summary = get_ai_sentiment(latest_news)
    
    # 將結果存入 data
    data[symbol] = {
        "news": latest_news,
        "ai_prediction": ai_summary,
        # ... 其他欄位
    }
    # ... (原有寫入 JSON 邏輯)
