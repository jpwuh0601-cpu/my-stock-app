import streamlit as st
import twstock
import pandas as pd
import random
import requests
import time
import threading
import schedule
from datetime import datetime

# 設定網頁標題
st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (全自動化版)")

# 初始化狀態
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# --- 核心邏輯函式 ---

def log_to_file(message):
    with open("daily_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {message}\n")

def send_line_message(token, message):
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)

def get_realtime_price(ticker):
    try:
        data = twstock.realtime.get(ticker)
        return float(data['realtime']['latest_trade_price'])
    except: return 0.0

def calculate_strategies(df):
    macd = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    signal = macd.ewm(span=9, adjust=False).mean()
    atr = (df['High'] - df['Low']).rolling(window=14).mean()
    return macd.iloc[-1], signal.iloc[-1], atr.iloc[-1]

def ai_score(macd, signal, atr, sentiment):
    score = 0
    if macd > signal: score += 50
    score += (sentiment * 5)
    if atr > 5: score -= 20
    return max(0, round(score))

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1)
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df['High'] = df['close'] * 1.02
        df['Low'] = df['close'] * 0.98
        df.rename(columns={'close': 'Close'}, inplace=True)
        return df
    except: return None

# --- 排程任務邏輯 ---

def scheduled_job():
    token = st.secrets.get("LINE_NOTIFY_TOKEN")
    report = "🤖 AI 自動化健檢報告 (每日定時)\n"
    for item in st.session_state.portfolio:
        df = fetch_data(item['代號'])
        score = ai_score(*calculate_strategies(df), random.randint(0,10)) if df is not None else 0
        status = "✅ 良好" if score >= 30 else "⚠️ 建議檢視"
        report += f"- {item['代號']}: 評分 {score} ({status})\n"
    send_line_message(token, report)
    log_to_file(report)

def run_scheduler():
    schedule.every().day.at("08:30").do(scheduled_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# 啟動背景執行緒 (在 app 啟動時自動觸發)
if 'scheduler_started' not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    st.session_state.scheduler_started = True

# --- UI 模組 ---

menu = st.sidebar.radio("核心模組", ["選股矩陣", "部位對帳單", "自動報告生成", "執行日誌"])
token = st.secrets.get("LINE_NOTIFY_TOKEN")

if menu == "選股矩陣":
    st.subheader("AI 產業掃描")
    # ... (選股矩陣邏輯維持原樣)

elif menu == "部位對帳單":
    st.subheader("我的投資組合")
    # ... (部位對帳單邏輯維持原樣)

elif menu == "自動報告生成":
    st.info("系統將於每日 08:30 自動推送。")
    if st.button("立即執行一次健檢推送"):
        scheduled_job()
        st.success("報告已推送。")

elif menu == "執行日誌":
    st.subheader("歷史決策記錄")
    try:
        with open("daily_log.txt", "r", encoding="utf-8") as f:
            st.text(f.read())
    except:
        st.write("目前尚無記錄。")
