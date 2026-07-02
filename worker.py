import json
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    # 嚴格讀取環境變數
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key or len(api_key) < 10:
        logging.error("❌ 嚴重錯誤：無法讀取 API Key，或是 Key 的長度異常短！")
        return

    logging.info(f"✅ API Key 格式檢查通過，開始發送請求...")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-flash-1.5-8b",
        "messages": [{"role": "user", "content": "簡單分析台積電 2330"}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        # 強制處理可能發生的空回應
        if response is None:
            logging.error("❌ 伺服器回傳空物件 (None)")
            return
            
        if response.status_code == 200:
            ai_result = response.json()['choices'][0]['message']['content']
        else:
            logging.error(f"❌ API 錯誤: {response.status_code}, 內容: {response.text}")
            ai_result = f"API 錯誤 {response.status_code}"
            
    except Exception as e:
        logging.error(f"❌ 請求過程發生錯誤: {str(e)}")
        ai_result = "連線失敗"

    data = {"ai_prediction": ai_result, "price": 1050.0}
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    logging.info("數據寫入完成。")

if __name__ == "__main__":
    run_analysis_and_update()
