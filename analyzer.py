import pandas as pd
import requests
import os

def fetch_market_sentiment(ticker_symbol):
    """獲取市場情緒：未來可串接新聞 API，目前為關鍵字對應"""
    sentiment_data = {
        "2330.TW": "外資持續買入，市場對先進製程預期樂觀。",
        "2317.TW": "鴻海電動車布局持續發酵，法人看法中性偏多。",
        "2454.TW": "手機晶片需求回溫，市場關注度高。"
    }
    return sentiment_data.get(ticker_symbol, "該個股目前市場無重大負面新聞，走勢平穩。")

def generate_ai_analysis(ticker_symbol, info, broker_data=None):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    pe = info.get('forwardPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    
    sentiment_report = fetch_market_sentiment(ticker_symbol)
    
    # 簡單計算籌碼趨勢
    broker_trend = "賣超"
    if broker_data:
        total_volume = sum([int(str(d['買賣張數']).replace(',', '')) for d in broker_data if isinstance(d['買賣張數'], (str, int))])
        if total_volume > 0: broker_trend = "買超"
    
    prompt = f"""
    請針對股票 {ticker_symbol} 進行綜合財經分析。
    基本面: PE {pe}, EPS {eps}。
    市場情緒: {sentiment_report}。
    籌碼面: 主力近期呈現 {broker_trend}。
    
    決策指示:
    1. 若「市場情緒負面」且「主力賣超」，標註「⚠️ 風險提示：強烈建議觀察或減碼」。
    2. 若「市場情緒樂觀」且「主力買超」，標註「🚀 強勢續抱：籌碼與市場情緒一致」。
    最後請給出一個 1-10 的樂觀情緒分數。
    """
    
    ai_result = call_llm(prompt, api_key) if api_key else "⚠️ API Key 未設定。"
    
    return {
        "main_force_analysis": ai_result
    }

def call_llm(prompt, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析服務錯誤: {e}"
