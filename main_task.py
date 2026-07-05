import json
import os
import yfinance as yf
from worker import fetch_real_broker_data
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file): return
    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    # 準備存放給 LINE 的最終通知訊息
    notify_report = ["📊 每日籌碼監控報告:"]
    
    for ticker in tickers:
        try:
            # 1. 取得股價與漲跌幅
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if len(hist) < 2: continue
            
            price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            change = ((price - prev_price) / prev_price) * 100
            
            # 2. 取得券商數據
            broker_data = fetch_real_broker_data(ticker)
            
            # 3. 判斷是否有異常 (若漲幅超過 3% 標記為 🔥，否則為 ✅)
            is_active = "🔥" if change > 3 else "✅"
            
            # 4. 產生分析摘要
            analysis = generate_ai_analysis(ticker, stock.info, broker_data=broker_data)
            
            notify_report.append(f"{is_active} [{ticker}] 現價:{price:.2f} 漲幅:{change:+.2f}%")
            
        except Exception as e:
            print(f"處理 {ticker} 發生錯誤: {e}")

    # 5. 發送整合訊息至 LINE
    if len(notify_report) > 1:
        send_line_notify("\n".join(notify_report))

if __name__ == "__main__":
    run_analysis()
