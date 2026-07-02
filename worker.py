import json
import os
import logging

# 設定日誌記錄，方便在 GitHub Actions 查看執行狀態
logging.basicConfig(level=logging.INFO)

def run_analysis_and_update():
    """執行市場數據分析並更新 JSON 檔案"""
    logging.info("開始執行數據分析流程...")
    
    # 這裡可放入您的 yfinance 抓取邏輯或 AI API 呼叫
    # 目前為示範數據，確保儀表板能完整呈現 10 筆主力券商與法人數據
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
            
            # 10 家主力券商 10 日累計買賣超
            "brokers_10d": [
                {"券商": "凱基台北", "10日累計": 5500},
                {"券商": "富邦", "10日累計": 2100},
                {"券商": "元大", "10日累計": -1500},
                {"券商": "永豐金", "10日累計": 1200},
                {"券商": "國泰", "10日累計": -800},
                {"券商": "群益", "10日累計": 950},
                {"券商": "華南永昌", "10日累計": 400},
                {"券商": "統一", "10日累計": -600},
                {"券商": "第一金", "10日累計": 300},
                {"券商": "兆豐", "10日累計": 200}
            ],
            
            "ai_prediction": "AI 分析: 籌碼面呈現集中趨勢，建議持續關注外資買盤動能。"
        }

        # 使用原子寫入機制，確保檔案不會因意外中斷而損毀
        temp_file = "market_data.json.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        
        # 覆蓋舊檔案
        os.replace(temp_file, "market_data.json")
        logging.info("market_data.json 已更新成功，包含 10 筆法人與券商數據")

    except Exception as e:
        logging.error(f"數據處理過程發生錯誤: {e}")
        raise e

if __name__ == "__main__":
    run_analysis_and_update()
