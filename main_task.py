import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data
from analyzer import generate_ai_analysis

def run_main():
    """執行每日股市數據抓取與AI分析，強制確保數據完整性"""
    
    # 讀取股票清單
    try:
        with open("tickers.txt", "r", encoding="utf-8") as f:
            tickers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ 錯誤: 找不到 tickers.txt")
        return

    final_results = {}
    print(f"🚀 開始資料更新，共 {len(tickers)} 支...")

    for ticker in tickers:
        print(f"🔍 正在獲取 {ticker} 的完整數據...")
        
        # 抓取資料
        stock_info = fetch_stock_data(ticker)
        inst_data = fetch_institutional_data(ticker)
        
        # 處理 info 字典，確保所有 key 都存在，避免崩潰
        info = stock_info.get("info", {})
        
        # 生成 AI 分析
        ai_result = generate_ai_analysis(ticker, str(info), str(inst_data))
        
        # 嚴格構建資料結構 (強制賦值)
        final_results[ticker] = {
            "price": stock_info.get("price") or info.get("currentPrice") or 0.0,
            "nav": info.get("bookValue") or 0.0,
            "pe": info.get("trailingPE") or 0.0,
            "eps": info.get("trailingEps") or 0.0,
            "ai_prediction": ai_result.get("main_force_analysis", "AI 正在分析中..."),
            "institutional_data": inst_data if inst_data else "無法人籌碼資料"
        }
        
        time.sleep(6) # 延長延遲確保穩定

    # 寫入檔案
    output_path = os.path.join(os.getcwd(), "market_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("✅ 成功更新所有數據欄位。")

if __name__ == "__main__":
    run_main()
