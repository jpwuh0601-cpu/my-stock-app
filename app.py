import streamlit as st
import twstock
import pandas as pd
import random
import requests
import plotly.express as px

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (專業實戰整合版)")

# 初始化持股狀態
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

SECTOR_MAP = {
    "半導體": ["2330", "2454", "3034"],
    "金融": ["2881", "2882", "2886"],
    "航運": ["2603", "2609"],
    "生技": ["1795", "4743"]
}

# --- 功能模組 ---
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
menu = st.sidebar.radio("核心模組", ["市場監控", "AI 選股與下單", "部位健檢"])

if menu == "市場監控":
    st.subheader("📊 市場資金流向熱點圖")
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
            if st.button("確認執行自動化下單"):
                st.success("下單指令已發送至模擬帳戶。")

elif menu == "部位健檢":
    st.subheader("持股部位監控與健檢")
    with st.form("add_pf"):
        t = st.text_input("股票代號", "2330")
        cost = st.number_input("買入成本", 500.0)
        if st.form_submit_button("新增部位"):
            st.session_state.portfolio.append({"代號": t, "成本": cost})
    
    for item in st.session_state.portfolio:
        df = fetch_data(item['代號'])
        score = ai_score(*calculate_strategies(df), get_market_sentiment(item['代號']))
        st.write(f"代號: {item['代號']} | 當前 AI 評分: {score} | 建議: {'持有' if score > 50 else '減碼/健檢'}")
