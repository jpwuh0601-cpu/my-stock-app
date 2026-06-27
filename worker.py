import twstock
import pandas as pd
import random
import requests
import os
from datetime import datetime

# --- 設定參數 ---
# 實際應用時建議將 TOKEN 設為環境變數
LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN", "YOUR_TOKEN_HERE")

# --- 核心邏輯 (從 app.py 抽出) ---
def get_market_sentiment(ticker):
    return random.uniform(-1, 1)

def calculate_strategies(df):
    macd = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    signal = macd.ewm(span=9, adjust=False).mean()
    atr = (df['High'] - df['Low']).rolling(window=14).mean()
    return macd.iloc[-1], signal.iloc[-1], atr.iloc[-1]

def ai_score(macd, signal, atr, sentiment):
    score = 50 + (macd - signal) * 10 + (sentiment * 20) - (atr * 2)
    return max(0, min(100, round(score)))

def fetch_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1)
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df['High'], df['Low'] = df['close'] * 1.02, df['close'] * 0.98
        df.rename(columns={'close': 'Close'}, inplace=True)
        return df
    except: return None

def send_line_message(token, message):
    if not token or token == "YOUR_TOKEN_HERE": return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)

def log_to_file(message):
    with open("daily_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {message}\n")

# --- 執行主任務 ---
def run_daily_job(portfolio):
    report = f"🤖 AI 自動化健檢報告 ({datetime.now().strftime('%Y-%m-%d')})\n"
    for item in portfolio:
        df = fetch_data(item['代號'])
        if df is not None:
            score = ai_score(*calculate_strategies(df), get_market_sentiment(item['代號']))
            status = "✅ 持有" if score >= 50 else "⚠️ 建議減碼"
            report += f"- {item['代號']}: 評分 {score} ({status})\n"
    
    send_line_message(LINE_TOKEN, report)
    log_to_file(report)

if __name__ == "__main__":
    # 這裡定義需要監控的持股清單
    # 實際部署可從資料庫或 JSON 檔讀取
    my_portfolio = [{"代號": "2330", "成本": 500.0}, {"代號": "2454", "成本": 1000.0}]
    run_daily_job(my_portfolio)
