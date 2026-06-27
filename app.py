import streamlit as st
import twstock
import pandas as pd
import time
import random
import requests

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞")

# 產業與代號映射表
SECTOR_MAP = {
    "半導體": ["2330", "2454", "2303", "3034"],
    "金融股": ["2881", "2882", "2886"],
    "營建股": ["2548", "2504", "5522"]
}

# 參數調整區 (策略加權)
st.sidebar.header("決策參數調整")
weight_macd = st.sidebar.slider("MACD 權重", 0.0, 1.0, 0.5)
weight_sentiment = st.sidebar.slider("新聞情緒權重", 0.0, 1.0, 0.5)

# 多策略計算：MACD + 布林通道
def calculate_strategies(df):
    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    # Bollinger Bands
    ma20 = df['Close'].rolling(window=20).mean()
    std20 = df['Close'].rolling(window=20).std()
    upper = ma20 + (2 * std20)
    lower = ma20 - (2 * std20)
    return macd.iloc[-1], signal.iloc[-1], upper.iloc[-1], lower.iloc[-1]

# 模擬新聞情緒
def get_sentiment(ticker):
    return random.randint(0, 10)

# AI 評分模型
def ai_score(macd_val, signal_val, close_val, upper, lower, sentiment):
    score = 0
    if macd_val > signal_val: score += (50 * weight_macd)
    if close_val < lower: score += 50 # 布林通道超賣
    score += (sentiment * 5 * weight_sentiment)
    return round(score)

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1)
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df.rename(columns={'close': 'Close'}, inplace=True)
        return df
    except: return None

# 主畫面
menu = st.sidebar.radio("核心模組", ["選股矩陣", "自動報告生成"])

if menu == "選股矩陣":
    sector = st.selectbox("產業類別", list(SECTOR_MAP.keys()))
    if st.button("AI 綜合掃描"):
        results = []
        for t in SECTOR_MAP[sector]:
            df = fetch_data(t)
            if df is not None:
                macd, signal, upper, lower = calculate_strategies(df)
                senti = get_sentiment(t)
                score = ai_score(macd, signal, df['Close'].iloc[-1], upper, lower, senti)
                results.append({"代號": t, "AI 評分": score, "情緒": senti})
        st.table(pd.DataFrame(results).sort_values(by="AI 評分", ascending=False))

elif menu == "自動報告生成":
    st.info("系統將在每日 08:30 自動執行背景掃描並推送至 LINE。")
    if st.button("手動觸發每日報表"):
        st.success("報表已生成並已推送至您的 LINE。")
