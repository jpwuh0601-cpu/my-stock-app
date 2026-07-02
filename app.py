import json
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

def get_ai_analysis(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "API Key 未設定"

    # 確保 URL 完全正確
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "Stock Analysis"
    }
    
    payload = {
        "model": "google/gemini-flash-1.5-8b",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # 強制檢查是否有內容
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                return "API 回傳格式異常"
        else:
            return f"API 錯誤: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"連線例外錯誤: {str(e)}"

def run_analysis_and_update():
    logging.info("開始執行數據分析...")
    ai_result = get_ai_analysis("請簡單分析台積電 2330 目前趨勢。")
    
    # 確保資料結構完整，避免前端報錯
    data = {
        "price": 1050.0,
        "pe_ratio": 32.5,
        "est_revenue": 2500000000000,
        "est_eps": 42.5,
        "est_dividend": 16.0,
        "margin_ratio": 1.15,
        "institutional_investors": [{"機構": "外資", "買賣超": 1000}],
        "top_brokers": [{"券商": "凱基", "買進": 500}],
        "ai_prediction": ai_result
    }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    logging.info("數據寫入完成。")

if __name__ == "__main__":
    run_analysis_and_update()
