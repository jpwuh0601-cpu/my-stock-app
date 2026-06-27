import streamlit as st
import pandas as pd
import random
import requests
import plotly.express as px
import os
from datetime import datetime

# 設定頁面
st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (專業實戰整合版)")

# 初始化狀態
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# --- 核心邏輯函式 ---
def send_line_message(token, message):
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)

def log_to_file(message):
    with open("daily_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {message}\n")

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
    import twstock
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
    SECTOR_MAP = {"半導體": ["2330"], "金融": ["2881"], "航運": ["2603"]}
    data = []
    for sector, tickers in SECTOR_MAP.items():
        avg_score = sum([ai_score(*calculate_strategies(fetch_data(t)), get_market_sentiment(t)) for t in tickers if fetch_data(t) is not None]) / len(tickers)
        data.append({"產業": sector, "平均強度": round(avg_score, 2)})
    fig = px.treemap(pd.DataFrame(data), path=['產業'], values='平均強度', color='平均強度', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "AI 選股與下單":
    st.subheader("AI 自動化決策")
    t = st.text_input("輸入股票代號", "2330")
    if st.button("評估買入"):
        df = fetch_data(t)
        score = ai_score(*calculate_strategies(df), get_market_sentiment(t))
        st.metric("AI 綜合決策分數", f"{score}/100")
        if score > 75:
            st.success("評分達標，建議買入！")

elif menu == "部位健檢":
    st.subheader("持股部位監控與健檢")
    with st.form("add_pf"):
        t = st.text_input("股票代號", "2330")
        cost = st.number_input("買入成本", 500.0)
        if st.form_submit_button("新增部位"):
            st.session_state.portfolio.append({"代號": t, "成本": cost})
    
    if st.button("執行全面健檢並推送至 LINE"):
        report = f"🚨 AI 持股健檢報告 ({datetime.now().strftime('%Y-%m-%d')})\n"
        for item in st.session_state.portfolio:
            df = fetch_data(item['代號'])
            score = ai_score(*calculate_strategies(df), get_market_sentiment(item['代號']))
            status = "✅ 持有" if score >= 50 else "⚠️ 建議減碼"
            report += f"- {item['代號']}: 評分 {score} ({status})\n"
        send_line_message(token, report)
        log_to_file(report)
        st.success("健檢報告已推送。")

elif menu == "決策日誌":
    st.subheader("📋 互動式決策歷史日誌")
    if os.path.exists("daily_log.txt"):
        with open("daily_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        df = pd.DataFrame([{"時間": l.split(":", 2)[0]+":"+l.split(":", 2)[1], "內容": l.split(":", 2)[2].strip()} for l in lines])
        search = st.text_input("🔍 搜尋歷史紀錄")
        if search: df = df[df['內容'].str.contains(search, case=False)]
        st.dataframe(df, use_container_width=True)
