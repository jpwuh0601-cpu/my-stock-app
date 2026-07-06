import json
import os
import time
from worker import fetch_stock_data, fetch_institutional_data

def run_main():
    """
    主要任務腳本：負責讀取股票清單，抓取資料並寫入 market_data.json。
    此腳本不應包含任何 UI (Streamlit) 相關模組。
    """
    ticker_file = "tickers.txt"
    if os.path.exists(ticker_file):
        with open(ticker_file, "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]

    final_results = {}
    print(f"DEBUG: 開始執行任務，處理目標: {tickers}")

    for ticker in tickers:
        try:
            print(f"DEBUG: 正在處理 {ticker}...")
            # 抓取股價與法人籌碼數據
            stock_data = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            
            # 將資料標準化，確保即使缺失也不會寫入 None 或非法結構
            # 數值皆轉為字串以確保 JSON 可序列化且前端顯示友善
            final_results[ticker] = {
                "price": str(stock_data.get("price", "0")),
                "eps": str(stock_data.get("eps", "0")),
                "nav": "0",  # 預留位
                "pe": "0",   # 預留位
                "institutional_data": inst_data if isinstance(inst_data, list) else [],
                "ai_prediction": "AI 分析生成中...",
                "news": "目前無最新即時新聞"
            }
            # 避免觸發 API 限制
            time.sleep(5) 
        except Exception as e:
            print(f"DEBUG: 處理 {ticker} 時發生錯誤: {e}")

    # 安全寫入 JSON，確保檔案結構為 UTF-8
    try:
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=4)
        print("DEBUG: market_data.json 已成功寫入。")
    except Exception as e:
        print(f"DEBUG: 檔案寫入失敗: {e}")

if __name__ == "__main__":
    run_main()
