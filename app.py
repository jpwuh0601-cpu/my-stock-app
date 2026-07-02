import json
import os
import requests
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

def get_ai_analysis(prompt):
    """修正後的 OpenRouter API 呼叫"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "API Key 未設定"

    # 調整 URL 和模型名稱
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/your-repo", # 建議加上這行，有些 API 要求此欄位
        "X-Title": "Stock Analysis App",
        "Content-Type": "application/json"
    }
    
    # 使用較為常見的模型名稱，避免 404
    payload = {
        "model": "google/gemini-flash-1.5-8b", 
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        # 顯示原始錯誤內容以利除錯
        if response.status_code != 200:
            logging.error(f"API 錯誤代碼: {response.status_code}, 回應: {response.text}")
            return f"分析失敗 (錯誤代碼 {response.status_code})"
            
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"例外錯誤: {e}")
        return "分析服務無法連接"

def run_analysis_and_update():
    logging.info("開始執行 OpenRouter 數據分析...")
    
    analysis_prompt = "請根據台灣股市台積電(2330)的現況給出簡短投資觀點。"
    ai_result = get_ai_analysis(analysis_prompt)
    
    # 模擬數據結構
    data = {
        "price": 230.0,
        "pe_ratio": 44.2,
        "est_revenue": 1200000,
        "est_eps": 5.2,
        "est_dividend": 3.5,
        "margin_ratio": 1.25,
        "institutional_investors": [{"機構": "外資", "買賣超": 500}, {"機構": "投信", "買賣超": -200}],
        "top_brokers": [
            {"券商": "凱基台北", "買進": 1000, "賣出": 200},
            {"券商": "富邦", "買進": 800, "賣出": 900}
        ],
        "ai_prediction": ai_result
    }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    logging.info("分析數據已更新至 market_data.json")

if __name__ == "__main__":
    run_analysis_and_update()
