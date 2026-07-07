import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def run_main():
    """
    執行每日股市數據抓取、AI 分析，並將結果儲存至 market_data.json
    """
    # 1. 從 tickers.txt 讀取所有需要分析的股票
    try:
        with open("tickers.txt", "r", encoding="utf-8") as f:
            tickers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ 錯誤: 找不到 tickers.txt")
        return

    final_results = {}
    print(f"🚀 開始執行數據更新任務，共 {len(tickers)} 支股票...")

    for ticker in tickers:
        print(f"🔍 正在分析: {ticker}")
        
        # 2. 抓取基礎股價與法人數據
        stock_info = fetch_stock_data(ticker)
        if "error" in stock_info:
            print(f"⚠️ 抓取 {ticker} 失敗: {stock_info['error']}")
            continue
            
        inst_data = fetch_institutional_data(ticker)
        
        # 3. 呼叫 AI 分析 (對接 analyzer.py)
        ai_result = generate_ai_analysis(
            ticker, 
            str(stock_info.get("info", {})), 
            str(inst_data)
        )
        
        # 4. 構建資料結構
        final_results[ticker] = {
            "price": stock_info.get("price", 0),
            "nav": stock_info.get("info", {}).get("bookValue", 0),
            "pe": stock_info.get("info", {}).get("trailingPE", 0),
            "eps": stock_info.get("eps", 0),
            "ai_prediction": ai_result.get("main_force_analysis", "無分析資訊"),
            "institutional_data": inst_data
        }
        
        # 避免觸發 API 頻率限制
        time.sleep(5)

    # 5. 強制寫入至根目錄的 market_data.json
    output_path = os.path.join(os.getcwd(), "market_data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print(f"✅ 成功寫入資料至: {output_path}")
    except Exception as e:
        print(f"❌ 寫入 JSON 失敗: {e}")

if __name__ == "__main__":
    run_main()
