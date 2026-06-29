import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 自動載入 .env 檔案中的設定
load_dotenv()

def calculate_investor_volume(broker_data):
    """
    計算大戶與散戶的買賣超。
    大戶標準：單一券商分點淨買賣超絕對值 > 400 張
    """
    big_investor_volume = 0
    retail_investor_volume = 0
    
    for broker in broker_data:
        net = broker.get('買進', 0) - broker.get('賣出', 0)
        if abs(net) > 400:
            big_investor_volume += net
        else:
            retail_investor_volume += net
            
    return big_investor_volume, retail_investor_volume

def run_analysis():
    # 初始化 OpenAI Client
    api_key = os.getenv("OPENROUTER_API_KEY")
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    # 模擬數據結構 (實際應用時請替換為 API 抓取邏輯)
    broker_data = [
        {"券商": "凱基", "買進": 500, "賣出": 0},
        {"券商": "富邦", "買進": 100, "賣出": 50}
    ]
    
    big_vol, retail_vol = calculate_investor_volume(broker_data)
    
    # 組合數據
    market_data = {
        "update_date": datetime.now().strftime("%Y-%m-%d"),
        "price": 230.5,
        "bvps": 150.2,
        "est_revenue": "10.5億",
        "est_eps": "5.2",
        "est_dividend": "3.5",
        "big_investor_volume": big_vol,
        "retail_investor_volume": retail_vol,
        "institutional_investors": [{"機構": "外資", "買賣超": 500}, {"機構": "自營商", "買賣超": -100}],
        "margin_ratio": 1.25,
        "top_brokers": broker_data,
        "ai_prediction": "AI 分析：預計未來趨勢呈現震盪向上，建議關注外資動向。",
        "news": ["公司獲利創新高", "市場信心增強"],
        "financials": {"2025Q1": {"EPS": 5.2, "淨值": 150.2}}
    }
    
    # 寫入 JSON
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(market_data, f, ensure_ascii=False, indent=4)
    print("分析完成，數據已更新至 market_data.json")

if __name__ == "__main__":
    run_analysis()
