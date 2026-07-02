import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_analysis_and_update():
    logging.info("開始執行分析任務...")
    
    # 定義完整的資料結構
    data = {
        "price": 230.0,
        "bvps": 150.2,
        "est_revenue": 1200000,
        "est_eps": 5.2,
        "est_dividend": 3.5,
        "margin_ratio": 1.25,
        "financials": {
            "2025Q1": {"EPS": 5.2, "淨值": 150.2},
            "2024Q4": {"EPS": 4.8, "淨值": 145.0}
        },
        "institutional_investors": [
            {"機構": "外資", "買賣超": 500},
            {"機構": "投信", "買賣超": -200},
            {"機構": "自營商", "買賣超": 50}
        ],
        "top_brokers": [
            {"券商": "凱基台北", "買進": 1000},
            {"券商": "富邦", "買進": 800}
        ],
        "news": ["最新測試新聞 1", "最新測試新聞 2"],
        "ai_prediction": "預測分析顯示該個股短期內有資金流入跡象。"
    }
    
    # 寫入檔案
    file_path = "market_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    logging.info(f"成功更新數據至: {file_path}")

if __name__ == "__main__":
    run_analysis_and_update()
