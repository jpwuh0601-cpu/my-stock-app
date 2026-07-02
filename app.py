import json
import os
import requests
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

def get_ai_analysis(prompt):
    """透過 OpenRouter API 呼叫 AI 進行分析"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logging.error("未找到 OPENROUTER_API_KEY")
        return "分析功能未啟用 (API Key 缺失)"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.0-flash-001",  # 您可以根據需求更換模型
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"OpenRouter API 呼叫失敗: {e}")
        return "分析服務暫時無法存取"

def run_analysis_and_update():
    """執行完整分析流程並寫入 market_data.json"""
    logging.info("開始執行 OpenRouter 數據分析...")
    
    # 這裡放入您實際的股價與財務數據獲取邏輯 (省略簡化)
    # 假設這是從 yfinance 或其他 API 取得的 raw_data
    
    # 呼叫 AI 進行深度分析
    analysis_prompt = "請根據台灣股市台積電(2330)的技術面與法人籌碼面數據，給出專業的投資觀點。"
    ai_result = get_ai_analysis(analysis_prompt)
    
    # 模擬數據結構
    data = {
        "price": 1050.0,
        "pe_ratio": 32.5,
        "est_revenue": 2500000000000,
        "est_eps": 42.5,
        "est_dividend": 16.0,
        "margin_ratio": 1.15,
        "institutional_investors": [
            {"機構": "外資", "買賣超": 12000},
            {"機構": "投信", "買賣超": 4500}
        ],
        "top_brokers": [
            {"券商": "美林", "買進": 5000, "賣出": 1000},
            {"券商": "瑞銀", "買進": 3000, "賣出": 2000}
        ],
        "ai_prediction": ai_result,
        "news": ["台積電營收創新高", "AI 供應鏈需求強勁"]
    }
    
    # 寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    logging.info("分析數據已更新至 market_data.json")

if __name__ == "__main__":
    run_analysis_and_update()
