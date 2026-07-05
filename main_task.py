import json
import yfinance as yf
import os
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    if not os.path.exists("tickers.txt"):
        print("找不到 tickers.txt")
        return

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    alert_messages = [] 
    
    for ticker in tickers:
        try:
            print(f"正在分析: {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 取得 AI 報告
            ai_report = generate_ai_analysis(ticker, info)
            price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            
            all_results[ticker] = {
                "price": price,
                "eps": info.get('trailingEps', 0),
                "pe": info.get('forwardPE', 0),
                "ai_prediction": ai_report,
                "news": "技術指標 (RSI/KD/MA) 分析完畢。",
                "black_swan": "安全" if info.get('trailingEps', 0) > 0 else "高風險"
            }
            
            # 優化通知邏輯：加入 emoji 與明確訊號
            if "積極買入" in ai_report:
                alert_messages.append(f"🚀 {ticker} 強力買進訊號!\n💰 現價: {price}\n📊 狀態: {ai_report}")
            elif "建議減碼" in ai_report:
                alert_messages.append(f"⚠️ {ticker} 減碼保護獲利!\n💰 現價: {price}\n📊 狀態: {ai_report}")
                
        except Exception as e:
            print(f"分析 {ticker} 時發生錯誤: {e}")

    # 儲存
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    # 統一發送
    if alert_messages:
        send_line_notify("\n\n" + "---\n".join(alert_messages))

if __name__ == "__main__":
    run_analysis()
