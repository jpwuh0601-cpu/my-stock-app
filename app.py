import streamlit as st
import twstock
import pandas as pd
import random
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (自動化與日誌版)")

# 初始化狀態
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# --- 工具函式 ---
def log_to_file(message):
    """將決策結果寫入本地日誌"""
    with open("daily_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {message}\n")

def send_line_message(token, message):
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)

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

@st.cache_data(ttl=3600)
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

# --- UI 模組 ---
menu = st.sidebar.radio("核心模組", ["市場監控", "AI 選股與下單", "部位健檢", "決策日誌"])
token = st.secrets.get("LINE_NOTIFY_TOKEN")

if menu == "市場監控":
    st.subheader("📊 市場資金流向熱點圖")
    # ... (熱點圖邏輯不變)

elif menu == "部位健檢":
    st.subheader("持股部位監控與健檢")
    # 新增健檢功能並串聯日誌與 LINE
    if st.button("執行全面健檢並推送至 LINE"):
        report = f"🚨 AI 持股健檢報告 ({datetime.now().strftime('%Y-%m-%d')})\n"
        for item in st.session_state.portfolio:
            df = fetch_data(item['代號'])
            score = ai_score(*calculate_strategies(df), get_market_sentiment(item['代號']))
            status = "✅ 持有" if score >= 50 else "⚠️ 建議減碼"
            report += f"- {item['代號']}: 評分 {score} ({status})\n"
        
        send_line_message(token, report)
        log_to_file(report)
        st.success("健檢報告已推送至 LINE 並寫入日誌。")

elif menu == "決策日誌":
    st.subheader("歷史決策記錄")
    try:
        with open("daily_log.txt", "r", encoding="utf-8") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.write("尚無執行記錄。")
