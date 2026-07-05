import json
import yfinance as yf
import os
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    if not os.path.exists("tickers.txt"):
        return

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 呼叫整合後的分析邏輯
            # 這裡我們模擬傳入數據，實際運作時可替換為真實的法人/新聞抓取模組
            report = generate_ai_analysis(ticker, info)
            
            all_results[ticker] = {
                "price": info.get('currentPrice', 0),
                "pe": info.get('forwardPE', 0),
                "eps": info.get('trailingEps', 0),
                "ai_prediction": report['ai_主力分析'],
                "black_swan": report['black_swan_report'],
                "institutional_table": report['institutional_table'].to_dict(orient='records') if hasattr(report['institutional_table'], 'to_dict') else [],
            }
        except Exception as e:
            print(f"分析 {ticker} 失敗: {e}")

    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    # 發送簡要通知
    send_line_notify("系統已完成每日籌碼分析，看板數據已更新。")

if __name__ == "__main__":
    run_analysis()
