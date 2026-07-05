import json
import argparse
from worker import fetch_stock_data, fetch_real_broker_data

def main():
    # 建立參數接收器
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True, help="股票代號")
    args = parser.parse_args()
    
    ticker = args.ticker
    print(f"DEBUG: 正在分析股票: {ticker}")

    try:
        # 獲取資料
        stock_info = fetch_stock_data(ticker)
        broker_info = fetch_real_broker_data(ticker)
        
        # 除錯：如果價格為 0，印出原始資訊以便檢查
        if stock_info.get("price", 0) == 0:
            print(f"WARNING: 無法獲取 {ticker} 的價格，請檢查代號格式是否正確 (需包含 .TW)")
            print(f"原始抓取數據: {stock_info}")

        final_data = {
            ticker: {
                "price": stock_info.get("price", 0),
                "ai_report": f"券商分析: {broker_info[0].get('券商', '無資料')}" if broker_info else "無資料",
                "raw_info": stock_info
            }
        }
        
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"SUCCESS: {ticker} 資料已寫入")
            
    except Exception as e:
        print(f"ERROR: 分析失敗: {e}")

if __name__ == "__main__":
    main()
