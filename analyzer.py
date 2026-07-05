import pandas as pd
import requests
import os

def fetch_market_sentiment(ticker_symbol):
    """
    獲取市場情緒：目前為基礎邏輯，未來可擴充為爬蟲或 API 串接
    """
    sentiment_data = {
        "2330.TW": "外資持續買入，市場對先進製程預期樂觀。",
        "2317.TW": "鴻海電動車布局持續發酵，法人看法中性偏多。",
        "2454.TW": "手機晶片需求回溫，市場關注度高。"
    }
    return sentiment_data.get(ticker_symbol, "該個股目前市場無重大負面新聞，走勢平穩。")

def generate_ai_analysis(ticker_symbol, info, broker_data=None):
    """
    綜合財經分析模組：結合基本面、籌碼與新聞情緒的決策加權版
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    pe = info.get('forwardPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    
    # 獲取新聞情緒
    sentiment_report = fetch_market_sentiment(ticker_symbol)
    
    # 計算籌碼趨勢 (簡單判斷主力是否買超)
    broker_trend = "賣超"
    if broker_data:
        # 簡單計算買賣張數總和，若大於 0 視為買超
        total_volume = sum([int(str(d['買賣張數']).replace(',', '')) for d in broker_data if isinstance(d['買賣張數'], (str, int))])
        if total_volume > 0:
            broker_trend = "買超"
    
    # 建構深度分析提示詞 (Prompt)
    prompt = f"""
    請針對股票 {ticker_symbol} 進行綜合財經分析。
    基本面: PE {pe}, EPS {eps}。
    市場情緒: {sentiment_report}。
    籌碼面: 主力近期呈現 {broker_trend}。
    
    決策指示:
    1. 若「市場情緒負面」且「主力賣超」，請在分析結論中明確標註「⚠️ 風險提示：強烈建議觀察或減碼」。
    2. 若「市場情緒樂觀」且「主力買超」，請在分析結論中明確標註「🚀 強勢續抱：籌碼與市場情緒一致」。
    3. 其他情況請給出中性分析。
    最後請給出一個 1-10 的情緒分數 (10 為最樂觀)。
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
