import json
import time
import os
from worker import fetch_stock_data, fetch_institutional_data, check_black_swan
from analyzer import check_geopolitical_risk, generate_ai_analysis

def run_main():
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file):
        print("tickers.txt 不存在，請檢查專案根目錄")
        return

    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    # 1. 執行全局風險分析 (地緣政治/Fed)
    geo_status, geo_reasons = check_geopolitical_risk()
    
    final_results = {}
    
    for ticker in tickers:
        print(f"正在分析: {ticker} ...")
        try:
            stock_data = fetch_stock_data(ticker)
            info = stock_data.get("info", {})
            
            # 2. 呼叫 AI 個股深度分析
            ai_report = generate_ai_analysis(ticker, str(info), "")
            
            # 3. 整合資料
            final_results[ticker] = {
                "price": stock_data.get("price", 0),
                "nav": info.get("bookValue", 0),
                "pe": info.get("trailingPE", 0),
                "eps": info.get("trailingEps", 0),
                "ai_report": ai_report.get("main_force_analysis", "分析中..."),
                "black_swan_global": geo_status,
                "black_swan_global_reasons": geo_reasons,
                "institutional_data": fetch_institutional_data(ticker),
                "last_update": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            time.sleep(8) # 避免 Yahoo Finance 限制
        except Exception as e:
            print(f"處理 {ticker} 失敗: {e}")

    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("完成更新")

if __name__ == "__main__":
    run_main()
