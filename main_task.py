import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def run_main():
    """
    執行每日股市數據抓取、AI 分析，並將結果儲存至 market_data.json
    """
    # 讀取股票代號
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    final_results = {}

    print(f"開始執行數據更新任務，共 {len(tickers)} 支股票...")

    for ticker in tickers:
        print(f"正在分析: {ticker}")
        
        # 1. 抓取股價與籌碼數據
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        
        # 2. 生成 AI 財報預測
        ai_result = generate_ai_analysis(
            ticker, 
            str(stock_info.get("info", {})), 
            str(inst_data)
        )
        
        # 3. 建立「平鋪結構」的 JSON 數據 (修正讀取困難的問題)
        final_results[ticker] = {
            "price": stock_info.get("price", 0),
            "nav": stock_info.get("info", {}).get("bookValue", 0),
            "pe": stock_info.get("info", {}).get("trailingPE", 0),
            "eps": stock_info.get("eps", 0),
            "ai_report": ai_result.get("main_force_analysis", "無分析資訊"),
            "institutional_data": inst_data
        }
        
        # 遵守 API 速率限制，避免被 Yahoo/OpenRouter 封鎖
        time.sleep(5)

    # 4. 強制寫入至專案根目錄
    output_path = os.path.join(os.getcwd(), "market_data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print(f"✅ 成功寫入資料至: {output_path}")
    except Exception as e:
        print(f"❌ 寫入 JSON 失敗: {e}")

if __name__ == "__main__":
    run_main()
