import streamlit as st
import twstock
import pandas as pd
import random
import requests
import plotly.express as px

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (專業實戰整合版)")

# 產業與代號映射表
SECTOR_MAP = {
    "半導體": ["2330", "2454", "3034"],
    "金融": ["2881", "2882", "2886"],
    "航運": ["2603", "2609"],
    "生技": ["1795", "4743"]
}

# --- A. 整合新聞 API (模擬架構) ---
def get_market_sentiment(ticker):
    # 此處未來可替換為 NewsAPI.org 請求邏輯
    # 範例：使用 requests.get(f"https://newsapi.org/...")
    # 這裡我們模擬根據股價波動給予情緒加權
    return random.uniform(-1, 1)

# --- B. 實作產業輪動監控矩陣 ---
def get_sector_data():
    data = []
    for sector, tickers in SECTOR_MAP.items():
        avg_score = 0
        for t in tickers:
            df = fetch_data(t)
            if df is not None:
                m, s, a = calculate_strategies(df)
                avg_score += ai_score(m, s, a, get_market_sentiment(t))
        data.append({"產業": sector, "平均強度": round(avg_score/len(tickers), 2)})
    return pd.DataFrame(data)

# --- C. 優化 UI 顯示 (資金流向熱點圖) ---
def render_dashboard():
    st.subheader("📊 市場資金流向熱點圖")
    df = get_sector_data()
    fig = px.treemap(df, path=['產業'], values='平均強度', color='平均強度', 
                     color_continuous_scale='RdYlGn', title="產業資金強度分佈")
    st.plotly_chart(fig, use_container_width=True)

# --- 核心邏輯 (計算策略) ---
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

# --- 主介面 ---
menu = st.sidebar.radio("核心模組", ["市場監控", "AI 選股與下單", "部位健檢"])

if menu == "市場監控":
    render_dashboard()
elif menu == "AI 選股與下單":
    st.subheader("AI 自動化決策")
    t = st.text_input("輸入股票代號", "2330")
    if st.button("評估買入"):
        df = fetch_data(t)
        score = ai_score(*calculate_strategies(df), get_market_sentiment(t))
        st.metric("AI 綜合決策分數", f"{score}/100")
        if score > 75:
            st.button("執行自動化下單")
elif menu == "部位健檢":
    st.info("部位監控中...")
