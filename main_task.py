import json
import os
import yfinance as yf
# 引入剛剛在 Canvas 中定義的分析邏輯
from analyzer import generate_ai_analysis

def run_analysis():
    # 1. 讀取 tickers.txt
    if not os.path.exists("tickers.txt"):
        print("錯誤：找不到 tickers.txt")
        return

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    
    # 2. 迴圈處理每一檔股票
    for ticker in tickers:
        print(f"正在分析: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 3. 呼叫 Canvas 中定義的 AI 分析邏輯
            # generate_ai_analysis 會自動計算 RSI/KD 並回傳格式化後的 Prompt
            ai_report = generate_ai_analysis(ticker, info)
            
            # 4. 彙整數據
            all_results[ticker] = {
                "price": info.get('currentPrice', 0),
                "eps": info.get('trailingEps', 'N/A'),
                "pe": info.get('forwardPE', 'N/A'),
                "ai_prediction": ai_report,
                "news": "已整合技術指標分析。"
            }
        except Exception as e:
            print(f"分析 {ticker} 時發生錯誤: {e}")

    # 5. 寫入 market_data.json
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print("所有股票分析完成，已寫入 market_data.json")

if __name__ == "__main__":
    run_analysis()
