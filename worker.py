import json
import os
import requests
import logging

# 設定日誌記錄，方便在 GitHub Actions 查看執行狀態
logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    """執行市場數據抓取、10日累計計算與 AI 分析"""
    logging.info("開始執行數據分析流程...")
    
    # 從環境變數讀取 API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logging.error("未設定 OPENROUTER_API_KEY")
        return

    # 此處為資料抓取與模擬處理邏輯
    # 您未來可在此處加入 yfinance 抓取歷史數據來計算 10 日累計
    try:
        result_data = {
            "price": 23000.0,
            "pe_ratio": 25.5,
            "bvps": 150.2,
            "margin_ratio": 1.25,
            "est_revenue": 850000000,
            "est_eps": 5.8,
            # 三大法人 10 日累計買賣超
            "institutional_10d": [
                {"機構": "外資", "10日累計": 12500},
                {"機構": "投信", "10日累計": 3200},
                {"機構": "自營商", "10日累計": -800}
            ],
            # 主力券商 10 日累計買賣
            "brokers_10d": [
                {"券商": "凱基台北", "10日累計": 5500},
                {"券商": "富邦", "10日累計": 2100},
                {"券商": "元大", "10日累計": -1500}
            ],
            "ai_prediction": "AI 分析: 籌碼面呈現集中趨勢，建議持續關注外資買盤動能。"
        }

        # 原子寫入：先寫入暫存檔再覆蓋，確保資料完整性
        temp_file = "market_data.json.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        
        # 替換舊檔案
        os.replace(temp_file, "market_data.json")
        logging.info("market_data.json 更新成功，包含法人與券商 10 日累計數據")

    except Exception as e:
        logging.error(f"數據處理過程發生錯誤: {e}")

if __name__ == "__main__":
    run_analysis_and_update()
