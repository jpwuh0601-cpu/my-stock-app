import requests
import os

def generate_ai_analysis(ticker_symbol, info, broker_data):
    """
    使用 OpenRouter API 進行財經數據深度分析
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return {"main_force_analysis": "⚠️ 錯誤: API Key 未設定，無法啟用 AI 分析。"}
    
    # 強化 Prompt，提供更專業的分析觀點
    prompt = f"""
    你是一位專業的台灣股市財經分析師。請針對股票 {ticker_symbol} 進行分析。
    基本面資訊: {info}
    近期籌碼數據 (主力券商買賣): {broker_data}
    
    請依據上述籌碼與基本面資料，提供以下分析建議 (繁體中文):
    1. 籌碼流向分析 (主力是否在吸籌或出貨)
    2. 短期走勢預判
    3. 操作建議 (買進、賣出或觀望)
    請保持專業且精簡。
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://streamlit.io/", # 建議填寫您的網址
        "X-Title": "Stock Analysis Bot"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        response.raise_for_status()
        
        # 獲取 AI 回應內容
        content = response.json()['choices'][0]['message']['content']
        return {"main_force_analysis": content}
        
    except Exception as e:
        return {"main_force_analysis": f"AI 分析服務錯誤: {str(e)}"}
