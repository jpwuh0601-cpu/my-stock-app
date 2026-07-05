import json
import yfinance as yf
import os
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file): return
    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    notify_messages = ["📊 今日籌碼分析摘要:"]

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 使用 worker.py 中整合的分析邏輯
            from worker import fetch_real_broker_data
            broker_data = fetch_real_broker_data(ticker)
            
            # 簡化報告
            report = generate_ai_analysis(ticker, info, broker_data=broker_data)
            
            all_results[ticker] = {
                "price": info.get('currentPrice', 0),
                "broker_table": broker_data
            }
            
            # 加入通知摘要
            top_broker = broker_data[0] if broker_data else {"券商": "無", "買賣張數": 0}
            notify_messages.append(f"\n[{ticker}] 主力券商: {top_broker['券商']} ({top_broker['買賣張數']}張)")
            
        except Exception as e:
            print(f"處理 {ticker} 失敗: {e}")

    # 寫入 JSON
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    # 發送豐富的 LINE 通知
    send_line_notify("\n".join(notify_messages))

if __name__ == "__main__":
    run_analysis()
