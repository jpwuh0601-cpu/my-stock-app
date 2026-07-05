import json
import os
from worker import fetch_stock_data, fetch_real_broker_data

def get_ticker_from_config():
    """讀取網頁端生成的 user_config.json"""
    config_path = "user_config.json"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                config = json.load(f)
                return config.get("ticker", "2330.TW")
            except:
                return "2330.TW"
    return "2330.TW"

def main():
    ticker = get_ticker_from_config()
    print(f"DEBUG: 正在分析股票: {ticker}")

    try:
        stock_info = fetch_stock_data(ticker)
        broker_info = fetch_real_broker_data(ticker)
        
        # 建立結構化資料
        final_data = {
            ticker: {
                "price": stock_info.get("price", 0),
                "ai_report": f"券商分析: {broker_info[0].get('券商', '無資料')}" if broker_info else "無資料",
                "raw_info": stock_info
            }
        }
        
        # 寫入 market_data.json
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"SUCCESS: 已更新 {ticker} 資料")
            
    except Exception as e:
        print(f"ERROR: 分析流程錯誤: {e}")

if __name__ == "__main__":
    main()
