import json
from datetime import datetime

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

# 之後在 worker.py 的執行邏輯最後，呼叫 save_market_data(final_data) 即可
