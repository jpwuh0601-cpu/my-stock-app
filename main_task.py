import json
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis

def get_tickers():
    return ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

def main():
    tickers = get_tickers()
    final_results = {}

    for ticker in tickers:
        print(f"正在分析: {ticker}...")
        # 取得資料
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        broker_data = fetch_top_brokers_data(ticker)
        
        # 進行 AI 分析
        ai_result = generate_ai_analysis(ticker, stock_info.get("info", {}), broker_data.to_dict('records'))
        
        # 將所有資料封裝進結果字典，確保沒有欄位為空
        final_results[ticker] = {
            "price": stock_info.get("price", 0),
            "institutional_data": inst_data if inst_data else [{"日期": "無資料", "外資": 0, "投信": 0, "自營商": 0}],
            "ai_prediction": ai_result.get("main_force_analysis", "分析暫時無法取得"),
            "last_update": "2026-07-06"
        }

    # 寫入檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("SUCCESS: JSON 檔案已更新，結構完整。")

if __name__ == "__main__":
    main()
