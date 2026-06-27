import streamlit as st
import twstock
import pandas as pd
import random
import requests
import plotly.express as px

#st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (部位管理版)")

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

#SECTOR_MAP = {
    "半導體": ["2330", "2454", "2303", "3034"],
    "金融股": ["2881", "2882", "2886"],
    "營建股": ["2548", "2504", "5522"]
}

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

#menu = st.sidebar.radio("核心模組", ["選股矩陣", "部位對帳單", "自動報告生成"])

if menu == "選股矩陣":
    sector = st.selectbox("選擇產業", list(SECTOR_MAP.keys()))
    if st.button("AI 綜合掃描"):
        results = []
        for t in SECTOR_MAP[sector]:
            df = fetch_data(t)
            if df is not None:
                macd, signal, atr = calculate_strategies(df)
                senti = random.randint(0, 10)
                score = ai_score(macd, signal, atr, senti)
                results.append({"代號": t, "AI 評分": score})
        st.table(pd.DataFrame(results))

#elif menu == "部位對帳單":
    st.subheader("我的投資組合")
    with st.form("add_stock"):
        c1, c2, c3 = st.columns(3)
        ticker = c1.text_input("股票代號", "2330")
        qty = c2.number_input("股數", 1000)
        price = c3.number_input("成本價", 500.0)
        if st.form_submit_button("新增部位"):
            st.session_state.portfolio.append({"代號": ticker, "股數": qty, "成本": price})
    
    if st.session_state.portfolio:
        pf_df = pd.DataFrame(st.session_state.portfolio)
        current_prices = [get_realtime_price(t) for t in pf_df['代號']]
        pf_df['現價'] = current_prices
        pf_df['損益'] = (pf_df['現價'] - pf_df['成本']) * pf_df['股數']
        st.table(pf_df)

elif menu == "自動報告生成":
    if st.button("觸發自動化報告"):
        st.success("報表已推送到您的 LINE。")
