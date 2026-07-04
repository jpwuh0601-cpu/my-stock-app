import yfinance as yf
import requests
import os

# 使用 OpenAI/OpenRouter 的 API 進行分析
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    news = ticker.news
    latest_news = news[0]['title'] if news else "目前無最新新聞報導"
    
    # 若無 API KEY 則回傳基礎分析
    if not api_key:
        return f"【{ticker_symbol} 市場觀點】: 成功獲取最新標題: {latest_news}。 (提示: 請於 Streamlit App Settings 設定 API Key 以啟用 AI 分析)"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": f"分析這則股市新聞的情緒：{latest_news}。請用一句話簡短總結市場觀點。"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析引擎暫時無法連線: {e}"
