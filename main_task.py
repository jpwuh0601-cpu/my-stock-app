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

    notify_messages = ["📊 今日監控報告:"]
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            info = stock.info
            
            # 計算漲跌幅
            price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            change = ((price - prev_price) / prev_price) * 100
            
            # 如果漲跌幅異常 (例如超過 3% 或低於 -3%)，加入警示
            alert = "🔥" if abs(change) > 3 else "✅"
            notify_messages.append(f"{alert} [{ticker}] {price:.2f} ({change:+.2f}%)")
            
        except Exception as e:
            print(f"處理 {ticker} 失敗: {e}")

    # 發送整合後的 LINE 通知
    send_line_notify("\n".join(notify_messages))

if __name__ == "__main__":
    run_analysis()
