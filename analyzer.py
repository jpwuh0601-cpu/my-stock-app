import pandas as pd
import requests
import os

# 模擬新聞抓取功能 (未來可串接 Google News API)
def fetch_stock_news(ticker_symbol):
    """取得該股票的簡單市場情緒 (此處示範使用搜尋關鍵字)"""
    # 實際運作時，這裡可以串接更複雜的新聞 RSS
    return "近期該股票於社群討論度上升，市場普遍關注其財報發布。"

def generate_ai_analysis(ticker_symbol, info, institutional_data=None, broker_data=None):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    pe = info.get('forwardPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    news = fetch_stock_news(ticker_symbol)
    
    prompt = f"""
    請針對股票 {ticker_symbol} 進行綜合財經分析。
    基本面: 本益比 {pe}, EPS {eps}。
    近期市場情緒與新聞: {news}。
    請綜合分析上述資訊，給出市場情緒分數 (1-10) 與投資建議。
    """
    
    ai_result = call_llm(prompt, api_key) if api_key else "⚠️ API Key 未設定。"
    
    return {
        "broker_table": pd.DataFrame(broker_data) if broker_data else pd.DataFrame(),
        "black_swan_report": {"report": "需串接即時新聞來源"},
        "main_force_analysis": ai_result
    }

def call_llm(prompt, api_key):
    """呼叫 OpenRouter API"""
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析服務錯誤: {e}"
