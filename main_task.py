import json
import yfinance as yf
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    # 讀取股票清單
    if not os.path.exists("tickers.txt"):
        print("找不到 tickers.txt")
        return

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    alert_messages = [] # 用於收集所有需要通知的訊號
    
    for ticker in tickers:
        try:
            print(f"正在分析: {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 呼叫 analyzer 模組進行 AI 分析
            ai_report = generate_ai_analysis(ticker, info)
            
            # 整合數據
            all_results[ticker] = {
                "price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                "eps": info.get('trailingEps', 0),
                "pe": info.get('forwardPE', 0),
                "ai_prediction": ai_report,
                "news": "已整合技術指標分析 (RSI/KD)。",
                "black_swan": "安全" if info.get('trailingEps', 0) > 0 else "高風險"
            }
            
            # 邏輯判斷：若 AI 建議含有「積極買入」，則加入通知清單
            if "積極買入" in ai_report:
                alert_messages.append(f"🚀 {ticker} 買入訊號通知！\n目前股價: {all_results[ticker]['price']}\n簡評: {ai_report[:60]}...")
                
        except Exception as e:
            print(f"分析 {ticker} 時發生錯誤: {e}")

    # 儲存數據至 JSON
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print("分析結果已更新至 market_data.json")
        
    # 如果有收集到通知訊號，統一發送 LINE 通知
    if alert_messages:
        print("偵測到買入訊號，正在發送 LINE 通知...")
        send_line_notify("\n\n".join(alert_messages))
    else:
        print("未偵測到積極買入訊號，無需發送通知。")

if __name__ == "__main__":
    import os
    run_analysis()
