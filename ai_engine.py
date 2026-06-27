import streamlit as st
import requests

def get_ai_analysis(stock_data):
    # 1. 使用 st.secrets 讀取金鑰
    # 請確保在 Streamlit Cloud 的 Secrets 頁面中，變數名稱為 OPENROUTER_API_KEY
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except KeyError:
        return "錯誤：找不到 API Key，請檢查 Streamlit Secrets 設定。"

    # 2. 設定 OpenRouter 要求的標準 Header
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://streamlit.io/", # OpenRouter 建議填入的應用網址
        "X-Title": "My Stock App"               # 您的應用名稱
    }

    # 3. 準備發送給 AI 的提示詞
    prompt = f"請分析這支股票的關鍵指標，並給予簡單的投資建議：{stock_data}"
    
    payload = {
        "model": "openai/gpt-3.5-turbo", # 您可以使用此模型或更換為其他型號
        "messages": [{"role": "user", "content": prompt}]
    }

    # 4. 發送請求
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        # 檢查回應狀態
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"AI 分析發生錯誤: Error code: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"程式執行時發生異常: {str(e)}"
