import json
import time
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    # 讀取目標股票清單
    try:
        with open("tickers.txt", "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
    except:
        tickers = ["2330.TW", "2317.TW", "2454.TW"]

    final_results = {}
    print(f"DEBUG: 開始執行任務，處理對象: {tickers}")

    for ticker in tickers:
        try:
            print(f"DEBUG: 正在處理 {ticker}...")
            stock_data = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            
            # 將資料標準化，確保即使缺失也不會寫入 None 或非法結構
            final_results[ticker] = {
                "price": str(stock_data.get("price", "0")),
                "eps": str(stock_data.get("eps", "0")),
                "nav": "0",  # 預留位
                "pe": "0",   # 預留位
                "institutional_data": inst_data if isinstance(inst_data, list) else [],
                "ai_prediction": "AI 分析生成中...",
                "news": "無最新資訊"
            }
            time.sleep(5) # 緩衝時間，避免被 Yahoo 封鎖
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 時發生錯誤: {e}")

    # 安全寫入 JSON
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("DEBUG: market_data.json 寫入成功。")
    except Exception as e:
        print(f"DEBUG: 檔案寫入失敗: {e}")

if __name__ == "__main__":
    run_main()
