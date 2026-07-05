import json
import os
from worker import fetch_stock_data, fetch_real_broker_data

def get_target_ticker():
    """
    邏輯：優先讀取網頁端生成的 user_config.json
    如果不存在，則回退到預設代號 2330.TW
    """
    config_path = "user_config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("ticker", "2330.TW")
        except Exception as e:
            print(f"讀取設定檔失敗，使用預設值: {e}")
            return "2330.TW"
    return "2330.TW"

def main():
    # 1. 取得目標股票代號
    ticker = get_target_ticker()
    print(f"DEBUG: 本次分析目標: {ticker}")

    # 2. 獲取資料
    try:
        stock_info = fetch_stock_data(ticker)
        broker_info = fetch_real_broker_data(ticker)
        
        # 3. 組建單一股票的資料結構
        # 為了相容您網頁端的讀取邏輯，我們維持 key 為 ticker 的格式
        final_data = {
            ticker: {
                "price": stock_info.get("price", 0),
                "ai_report": f"券商分析: {broker_info[0].get('券商', '無資料')}" if broker_info else "無資料",
                "raw_info": stock_info
            }
        }
        
        # 4. 寫入 JSON
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        
        print(f"SUCCESS: {ticker} 資料已寫入 market_data.json")
            
    except Exception as e:
        print(f"ERROR: 分析流程執行失敗: {e}")

if __name__ == "__main__":
    main()
