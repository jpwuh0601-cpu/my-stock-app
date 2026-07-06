import json
import os
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def get_tickers():
    """從 tickers.txt 讀取股票代號清單"""
    try:
        with open("tickers.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["2330.TW"]

def main():
    tickers = get_tickers()
    final_results = {}

    for ticker in tickers:
        print(f"正在執行分析任務: {ticker}...")
        try:
            # 1. 取得市場資料
            stock_info = fetch_stock_data(ticker)
            inst_data = fetch_institutional_data(ticker)
            broker_data = fetch_top_brokers_data(ticker)
            
            if "error" in stock_info:
                print(f"資料讀取失敗: {ticker}")
                continue

            # 2. 進行 AI 深度分析
            ai_result = generate_ai_analysis(ticker, stock_info.get("info", {}), broker_data.to_dict('records'))
            analysis_text = ai_result.get("main_force_analysis", "")
            
            # 3. 判斷並發送通知 (告警邏輯)
            # 若 AI 分析內容出現關鍵買進訊號，則自動發送 LINE 通知
            if "買進" in analysis_text or "吸籌" in analysis_text:
                send_line_notify(f"【關鍵訊號通知】{ticker} \n建議: {analysis_text[:100]}...")
            
            # 4. 存入結果
            final_results[ticker] = {
                "price": stock_info.get("price", 0),
                "ai_prediction": analysis_text,
                "last_update": "2026-07-06"
            }
        except Exception as e:
            print(f"處理 {ticker} 時發生錯誤: {e}")

    # 5. 寫入 market_data.json，供網頁前端使用
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("SUCCESS: 數據已更新並執行通知檢查")

if __name__ == "__main__":
    main()
