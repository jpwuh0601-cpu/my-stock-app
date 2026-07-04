import yfinance as yf
import requests
import os

# 使用 OpenAI/OpenRouter 的 API 進行分析
def get_ai_analysis(ticker_symbol):
    api_key = os.getenv("OPENROUTER_API_KEY")
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    news = ticker.news
    latest_news = news[0]['title'] if news else "目前無最新新聞報導"
    
    # 強化版分析提示詞 (Prompt)，納入財務比率判斷
    prompt = f"""
    請針對 {ticker_symbol} 進行專業財報分析。
    當前數據:
    - EPS: {info.get('trailingEps', 'N/A')}
    - 本益比 (PE): {info.get('forwardPE', 'N/A')}
    - 最新新聞: {latest_news}
    
    分析要求:
    1. 綜合評估該股票當前的估值是否過高。
    2. 結合新聞情緒判斷短期市場趨勢。
    3. 給出一個簡短的投資建議（買入/觀望/賣出）並解釋原因。
    """
    
    if not api_key:
        return f"【{ticker_symbol} 基礎觀點】: 成功獲取最新標題: {latest_news}。 (提示: 請於設定中加入 API Key 以啟用深度分析)"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析引擎暫時無法連線: {e}"
