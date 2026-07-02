import json
import logging

def run_analysis_and_update():
    # 更新資料結構：移除自營商，擴充為 10 個主力券商
    data = {
        "price": 230.0,
        "bvps": 150.2,
        "pe_ratio": 44.2,
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
            {"券商": "凱基台北", "買進": 1000, "賣出": 200},
            {"券商": "富邦", "買進": 800, "賣出": 900},
            {"券商": "元大", "買進": 700, "賣出": 300},
            {"券商": "永豐金", "買進": 650, "賣出": 400},
            {"券商": "國泰", "買進": 600, "賣出": 500},
            {"券商": "兆豐", "買進": 550, "賣出": 150},
            {"券商": "群益", "買進": 500, "賣出": 600},
            {"券商": "華南永昌", "買進": 450, "賣出": 350},
            {"券商": "第一金", "買進": 400, "賣出": 250},
            {"券商": "中國信託", "買進": 350, "賣出": 100}
        ],
        "news": ["測試新聞"],
        "ai_prediction": "數據顯示正常。"
    }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    run_analysis_and_update()
