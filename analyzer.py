import requests
import os
import json

def check_geopolitical_risk():
    """
    呼叫 AI 分析當日頭條新聞，判斷地緣政治風險 (俄烏、美伊、聯準會)
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return "安全", ["AI API 金鑰未設定，無法執行風險分析"]

    # 模擬新聞抓取 (實際生產環境建議整合 NewsAPI 或其他新聞源)
    news_context = "今日重點：俄烏衝突持續升級，中東地區美伊關係緊張，市場關注本週聯準會利率會議是否釋出鷹派訊號。"
    
    prompt = f"""
    請擔任專業財經風險分析師。根據以下新聞概要進行評估："{news_context}"
    
    評估重點：
    1. 俄烏戰爭升溫程度
    2. 美伊衝突擴散風險
    3. 聯準會 (Fed) 貨幣政策偏向 (鷹派/鴿派)
    
    若上述議題顯示「衝突升級」、「緊張」或「鷹派」訊號，請將整體評級定為「⚠️ 警示中」。
    請務必以 JSON 格式回傳，結構如下：
    {{
      "status": "安全" 或 "⚠️ 警示中",
      "reasons": ["原因1", "原因2", "原因3"]
    }}
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://streamlit.io/",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        data = response.json()
        
        if "choices" in data:
            content = data['choices'][0]['message']['content']
            result = json.loads(content)
            return result.get("status", "安全"), result.get("reasons", ["無特別分析內容"])
        else:
            return "安全", ["API 回傳格式異常"]
            
    except Exception as e:
        return "安全", [f"AI 分析服務異常: {str(e)}"]

def generate_ai_analysis(ticker, info_str, news_str):
    """
    保留原本的 AI 財報分析函式
    """
    # 此處可加入您的財報分析邏輯
    return {"main_force_analysis": "分析服務連線中，目前尚未讀取到財報數據。"}
