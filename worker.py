import json
import os
import requests
import logging

# 設定日誌等級為 DEBUG，以便在 Actions 中看到完整錯誤資訊
logging.basicConfig(level=logging.DEBUG)

def get_ai_analysis(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logging.error("API Key 遺失，請檢查 GitHub Secrets")
        return "分析功能未啟用"

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
        # 加入 timeout 並確保請求正確執行
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        logging.debug(f"回應狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            logging.error(f"API 回應失敗: {response.status_code}, 內容: {response.text}")
            return f"分析服務失敗 (Code: {response.status_code})"
            
    except Exception as e:
        logging.exception("發生請求異常:")
        return f"連線錯誤: {str(e)}"

def run_analysis_and_update():
    logging.info("開始數據分析流程...")
    ai_result = get_ai_analysis("請簡單分析台積電 2330 目前趨勢。")
    
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
        
    logging.info("market_data.json 已更新")

if __name__ == "__main__":
    run_analysis_and_update()
