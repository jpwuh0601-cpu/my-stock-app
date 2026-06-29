import json
import requests
import os
from datetime import datetime

def send_line_notify(message):
    """發送 LINE 通知"""
    token = os.getenv("LINE_NOTIFY_TOKEN")
    if not token:
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    try:
        requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")

def save_market_data(data):
    """確保數據在寫入前格式正確，並包含所有 app.py 要求的欄位"""
    required_keys = [
        'price', 'bvps', 'financials', 'institutional_investors', 
        'news', 'technical_indicators', 'est_revenue', 'est_eps', 
        'est_dividend', 'ai_prediction', 'margin_ratio', 
        'black_swan_alert', 'ai_stock_selection'
    ]
    
    # 加入更新時間
    data['update_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 補足缺失欄位以防儀表板報錯 (提供預設值)
    for key in required_keys:
        if key not in data:
            data[key] = "數據尚未更新"
            
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_analysis_and_update():
    """執行完整分析邏輯的主程式"""
    # 1. 這裡執行您的數據抓取 (yfinance, etc.)
    # 2. 這裡執行您的 AI 分析 (OpenAI/OpenRouter)
    # 3. 準備 final_data 字典
    
    final_data = {
        "price": 230.0, # 範例數據
        "bvps": 150.2,
        "financials": {"2025Q1": {"EPS": 5.2, "淨值": 150.2}},
        "institutional_investors": [{"機構": "外資", "買賣超": 500}],
        "news": ["測試新聞 1"],
        "technical_indicators": "強勢多頭格局",
        "est_revenue": "1000億",
        "est_eps": "25.0",
        "est_dividend": "10.0",
        "ai_prediction": "預計未來一週震盪走高",
        "margin_ratio": 1.25,
        "black_swan_alert": {"is_triggered": False, "reason": "無"},
        "ai_stock_selection": "推薦關注半導體龍頭"
    }
    
    # 儲存數據
    save_market_data(final_data)
    
    # 發送通知
    send_line_notify(f"每日股市分析已更新: {final_data['ai_prediction']}")

if __name__ == "__main__":
    run_analysis_and_update()
