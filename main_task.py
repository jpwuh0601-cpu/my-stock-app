import json
import os
import yfinance as yf
from worker import fetch_real_broker_data
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    # 確保 API Key 被正確讀取
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("警告: 環境變數中未發現 OPENROUTER_API_KEY")

    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file): return
    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    notify_messages = ["📊 每日投資秘書報告:"]

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 1. 抓取籌碼
            broker_data = fetch_real_broker_data(ticker)
            
            # 2. 進行深度分析 (將 API Key 隱性傳遞給 analyzer)
            analysis = generate_ai_analysis(ticker, info, broker_data=broker_data)
            
            all_results[ticker] = {
                "price": info.get('currentPrice', 0),
                "ai_report": analysis['main_force_analysis']
            }
            
            notify_messages.append(f"✅ [{ticker}] 分析完成")
        except Exception as e:
            print(f"處理 {ticker} 時發生錯誤: {e}")

    # 3. 儲存結果
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    # 4. 發送通知
    send_line_notify("\n".join(notify_messages))

if __name__ == "__main__":
    run_analysis()
