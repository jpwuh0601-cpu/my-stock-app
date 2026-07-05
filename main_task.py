import json
import yfinance as yf
import os
import pandas as pd
from analyzer import generate_ai_analysis
from notifier import send_line_notify

def run_analysis():
    # 確保 tickers.txt 存在
    ticker_file = "tickers.txt"
    if not os.path.exists(ticker_file):
        print("未找到 tickers.txt")
        return

    with open(ticker_file, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    all_results = {}
    for ticker in tickers:
        print(f"正在處理: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 準備模擬籌碼數據 (未來可替換為真實 API 抓取)
            mock_inst = [{"日期": "2026-07-04", "外資": 1500, "投信": 200, "自營商": -50}]
            mock_broker = [{"日期": "2026-07-04", "券商": "元大", "買賣張數": 800}]
            
            # 呼叫整合後的分析邏輯
            report = generate_ai_analysis(ticker, info, mock_inst, mock_broker, ["無重大黑天鵝風險"])
            
            # 建構存入 market_data.json 的結構
            all_results[ticker] = {
                "price": info.get('currentPrice', 0),
                "pe": info.get('forwardPE', 0),
                "eps": info.get('trailingEps', 0),
                "ai_prediction": report['main_force_analysis'],
                "black_swan": report['black_swan_report']['report'],
                "institutional_table": report['institutional_table'].to_dict(orient='records'),
                "broker_table": report['broker_table'].to_dict(orient='records')
            }
        except Exception as e:
            print(f"分析 {ticker} 失敗: {e}")

    # 寫入 JSON 供看板讀取
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
        
    # 發送通知
    send_line_notify("系統已完成每日籌碼與風險分析，看板數據已更新。")

if __name__ == "__main__":
    run_analysis()
