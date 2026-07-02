import json
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    # 檢查 Secret 是否載入
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logging.error("❌ 無法從 GitHub Secrets 讀取 OPENROUTER_API_KEY")
        return
    else:
        logging.info(f"✅ API Key 已載入 (長度: {len(api_key)})")

    # URL 與 Headers
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "Stock Analysis"
    }
    
    payload = {
        "model": "google/gemini-flash-1.5-8b",
        "messages": [{"role": "user", "content": "簡單分析台積電趨勢"}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            logging.info("成功獲取 AI 分析結果")
            ai_result = response.json()['choices'][0]['message']['content']
        else:
            logging.error(f"API 拒絕請求 (Code: {response.status_code})。請確認 API Key 權限。")
            ai_result = "API 存取被拒"
            
    except Exception as e:
        logging.error(f"連線錯誤: {e}")
        ai_result = "連線錯誤"

    # 寫入資料
    data = {"ai_prediction": ai_result, "price": 1050.0}
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    logging.info("資料更新完成")

if __name__ == "__main__":
    run_analysis_and_update()
