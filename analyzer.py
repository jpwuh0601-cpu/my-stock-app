import pandas as pd
import requests
import os

def fetch_market_sentiment(ticker_symbol):
    """
    透過外部資料源或簡單邏輯獲取市場情緒
    """
    # 這裡未來可整合 Google News API 或 RSS 爬蟲
    # 目前先以 ticker_symbol 進行關鍵字判定
    return "近期該股票於社群討論度上升，市場普遍關注其財報發布。"

def generate_ai_analysis(ticker_symbol, info, broker_data=None):
    """
    綜合財經分析模組：結合基本面、籌碼與新聞情緒
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    pe = info.get('forwardPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    
    # 獲取新聞情緒
    sentiment_report = fetch_market_sentiment(ticker_symbol)
    
    # 建構深度分析提示詞 (Prompt)
    prompt = f"""
    請針對股票 {ticker_symbol} 進行綜合財經分析。
    基本面: 本益比 {pe}, EPS {eps}。
    市場情緒與新聞: {sentiment_report}。
    籌碼面: 根據券商數據 {broker_data}，請分析主力動向。
    
    請綜合上述資訊，給出投資建議，並給出一個 1-10 的情緒分數 (10 為最樂觀)。
    請輸出結構化的分析報告。
    """
    
    ai_result = call_llm(prompt, api_key) if api_key else "⚠️ API Key 未設定。"
    
    return {
        "broker_table": pd.DataFrame(broker_data) if broker_data else pd.DataFrame(),
        "sentiment_report": sentiment_report,
        "main_force_analysis": ai_result
    }

def call_llm(prompt, api_key):
    """呼叫 OpenRouter API 執行深度分析"""
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析服務暫時無法連線: {e}"
