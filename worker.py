import yfinance as yf
import requests
import json
import os

# 將這裡替換為您的 LINE Notify Token
LINE_TOKEN = "YOUR_TOKEN_HERE"

def send_line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    requests.post(url, headers=headers, data={"message": message})

def run_analysis_and_update():
    tickers = ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
    data = {}
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price_change = info.get("regularMarketChangePercent", 0)
            
            # 黑天鵝判定與觸發推播
            is_risk = price_change <= -3.0
            black_swan = "⚠️ 高風險警示" if is_risk else "安全"
            
            if is_risk:
                send_line_notify(f"【警報】{symbol} 發生黑天鵝風險！跌幅已達 {round(price_change, 2)}%")

            data[symbol] = {
                "price": info.get("currentPrice") or 0,
                "change": round(price_change, 2),
                "eps": info.get("trailingEps") or 0,
                "pe": info.get("forwardPE") or 0,
                "black_swan": black_swan,
                "institutional_data": [{"日期": "最新", "外資": 0, "投信": 0, "自營商": 0}]
            }
        except Exception as e:
            print(f"[-] {symbol} 抓取錯誤: {e}")
            
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_analysis_and_update()
