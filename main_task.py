import json
import os
import yfinance as yf
from analyzer import generate_ai_analysis
from notifier import send_line_notify # 引入通知模組

def run_analysis():
    if not os.path.exists("tickers.txt"):
        return

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    alert_messages = [] # 儲存需要通知的內容
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            ai_report = generate_ai_analysis(ticker, info)
            
            all_results[ticker] = {
                "price": info.get('currentPrice', 0),
                "eps": info.get('trailingEps', 'N/A'),
                "pe": info.get('forwardPE', 'N/A'),
                "ai_prediction": ai_report,
                "news": "已整合技術指標分析。"
            }
            
            # 若 AI 建議含有積極買入，加入通知清單
            if "積極買入" in ai_report:
                alert_messages.append(f"【買入訊號】{ticker} 建議積極買入！")
        except Exception as e:
            print(f"分析 {ticker} 時發生錯誤: {e}")

    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    # 如果有通知需求，統一發送
    if alert_messages:
        send_line_notify("\n".join(alert_messages))

if __name__ == "__main__":
    run_analysis()
