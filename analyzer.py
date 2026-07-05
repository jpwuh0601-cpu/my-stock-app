import pandas as pd
import requests
import os

def generate_ai_analysis(ticker_symbol, info, institutional_data=None, broker_data=None, news_headlines=None):
    """
    透過 OpenRouter API 進行真實的財經分析
    """
    # 從環境變數讀取 API Key (請確保在 GitHub Secrets 設定了 OPENROUTER_API_KEY)
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    # 基本面數據準備
    pe = info.get('forwardPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    
    # 準備分析提示詞
    prompt = f"""
    請針對股票 {ticker_symbol} 進行深度財經分析。
    基本面數據: 本益比(PE) {pe}, 每股盈餘(EPS) {eps}。
    請給出買賣策略建議與黑天鵝風險評分。請用繁體中文回答。
    """
    
    # 若有 API KEY 則進行真實呼叫，否則使用基礎邏輯
    if api_key:
        ai_result = call_llm(prompt, api_key)
    else:
        ai_result = "⚠️ 尚未設定 OPENROUTER_API_KEY，無法執行 AI 深度分析。"
        
    return {
        "institutional_table": pd.DataFrame(institutional_data) if institutional_data else pd.DataFrame(),
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
        return f"AI 分析服務暫時無法連線: {e}"
