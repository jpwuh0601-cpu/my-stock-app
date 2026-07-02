import json
import os
import requests
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    """執行市場數據抓取與 AI 分析"""
    logging.info("開始執行 OpenRouter 數據分析...")
    
    # 從環境變數讀取 API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logging.error("未設定 OPENROUTER_API_KEY")
        return

    # OpenRouter API 設定
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-username/my-stock-app", # 可選，增加識別度
        "X-Title": "Stock Analysis App"
    }

    payload = {
        "model": "openai/gpt-4o-mini", # 確保模型名稱正確，OpenRouter 格式為 provider/model
        "messages": [{"role": "user", "content": "請分析當前股市趨勢..."}]
    }

    try:
        # 呼叫 API
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # 檢查是否為 404 或其他錯誤
        if response.status_code != 200:
            logging.error(f"OpenRouter API 呼叫失敗: {response.status_code} {response.text}")
            return

        # 假設分析完成，整理資料 (這裡需對應您的資料格式)
        result_data = {
            "price": 1050.0,
            "pe_ratio": 15.5,
            "bvps": 120.0,
            "margin_ratio": 1.5,
            "est_revenue": 5000000,
            "est_eps": 5.2,
            "institutional_investors": [{"機構": "外資", "買賣超": 500}],
            "top_brokers": [{"券商": "凱基", "買進": 1000}],
            "ai_prediction": "AI 分析結果已更新。"
        }

        # 寫入檔案：使用暫存檔防止損毀
        temp_file = "market_data.json.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        
        # 覆蓋舊檔
        os.replace(temp_file, "market_data.json")
        logging.info("市場數據已更新至 market_data.json")

    except Exception as e:
        logging.error(f"執行期間發生錯誤: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
