import yfinance as yf
import json
import os

def run_task():
    # 設定目標股票，此處以台積電為例
    ticker = "2330.TW"
    print(f"正在分析: {ticker}")
    
    # 初始化資料字典
    data = {
        "status": "success", 
        "ticker": ticker,
        "message": "數據已更新"
    }
    
    # 使用 yfinance 取得簡單數據範例 (若需要更詳細資訊可參考 worker.py)
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        data["price"] = info.get("currentPrice", 0)
        data["change"] = info.get("regularMarketChange", 0)
    except Exception as e:
        print(f"數據獲取失敗: {e}")
        data["status"] = "error"
        data["error"] = str(e)
    
    # 將數據寫入 JSON 檔案
    # 確保 market_data.json 位於專案根目錄
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("數據已成功寫入 market_data.json")

if __name__ == "__main__":
    # 執行任務
    run_task()
