import json
import logging

def run_analysis_and_update():
    # 確保包含 app.py 需要的所有欄位，避免 KeyError
    data = {
        "price": 230.0,
        "bvps": 150.2,
        "pe_ratio": 44.2,  # 新增：本益比
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
            {"機構": "投信", "買賣超": -200}
        ],
        "top_brokers": [
            {"券商": "凱基台北", "買進": 1000, "賣出": 200}, # 擴充欄位
            {"券商": "富邦", "買進": 800, "賣出": 900}
        ],
        "news": ["測試新聞"],
        "ai_prediction": "數據顯示正常。"
    }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    run_analysis_and_update()
