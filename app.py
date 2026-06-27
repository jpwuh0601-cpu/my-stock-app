import streamlit as st
import twstock
import pandas as pd
import time
import random
import requests
import matplotlib.pyplot as plt
import io

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業台股 AI 決策系統 (含新聞情緒分析)")

# 產業與代號映射表
SECTOR_MAP = {
    "半導體": ["2330", "2454", "2303", "3034", "6669"],
    "金融股": ["2881", "2882", "2886", "2891"],
    "營建股": ["2548", "2504", "5522"],
    "航運股": ["2603", "2609", "2615"]
}

# 簡易新聞情緒分析 (模擬抓取與分析)
def get_news_sentiment(ticker):
    # 實際應用中可使用 Google News API，這裡以模擬詞庫分析作為示範
    positive_words = ["獲利", "成長", "創新高", "優於預期", "展望佳"]
    negative_words = ["裁員", "虧損", "下調", "風險", "衰退"]
    
    # 模擬獲取新聞標題
    news_titles = [f"{ticker} 業績亮眼創新高", f"{ticker} 市場展望佳", "產業波動影響風險增加"]
    
    score = 0
    for title in news_titles:
        for p in positive_words:
            if p in title: score += 5
        for n in negative_words:
            if n in title: score -= 5
    return score # 返回情緒分數

# AI 綜合評分函數 (整合情緒分析)
def score_stock(df, win_rate, sentiment_score):
    score = 0
    # 1. MACD 強度 (30分)
    if df['MACD'].iloc[-1] > df['Signal'].iloc[-1]:
        score += 30
    # 2. RSI 動能 (20分)
    rsi = df['RSI'].iloc[-1]
    if 30 < rsi < 70:
        score += 20
    # 3. 回測績效 (20分)
    score += min(max(win_rate * 2, 0), 20)
    # 4. 新聞情緒 (30分)
    score += min(max(sentiment_score * 3, 0), 30)
    return round(score)

# MACD 回測邏輯
def perform_backtest(df):
    df['Signal_Cross'] = (df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))
    returns = []
    for i in range(len(df)):
        if df['Signal_Cross'].iloc[i] and i + 5 < len(df):
            ret = (df['Close'].iloc[i+5] - df['Close'].iloc[i]) / df['Close'].iloc[i]
            returns.append(ret)
    return round(sum(returns) / len(returns) * 100, 2) if returns else 0.0

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    time.sleep(random.uniform(0.5, 1.0))
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1) 
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df.rename(columns={'close': 'Close'}, inplace=True)
        
        if len(df) >= 26:
            delta = df['Close'].diff()
            df['RSI'] = 100 - (100 / (1 + (delta.where(delta > 0, 0).rolling(14).mean() / (-delta.where(delta < 0, 0).rolling(14).mean()))))
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df
    except:
        return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "產業選股矩陣"])

if menu == "產業選股矩陣":
    sector = st.selectbox("選擇產業類別", list(SECTOR_MAP.keys()))
    if st.button("開始 AI 綜合掃描 (含新聞情緒)"):
        results = []
        for t in SECTOR_MAP[sector]:
            df = fetch_data(t)
            if df is not None:
                win_rate = perform_backtest(df)
                sentiment = get_news_sentiment(t)
                score = score_stock(df, win_rate, sentiment)
                results.append({
                    "代號": t, 
                    "AI 綜合評分": score,
                    "情緒得分": sentiment,
                    "回測績效%": win_rate
                })
        
        res_df = pd.DataFrame(results).sort_values(by="AI 綜合評分", ascending=False)
        st.subheader(f"{sector} 產業 AI 推薦清單")
        st.table(res_df)

elif menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號", "2330")
    if st.button("查詢"):
        data = fetch_data(ticker)
        if data is not None:
            st.line_chart(data[['Close', 'MA20']])
