import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    """帶有重試機制的資料獲取函數"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 移除 pdr_override，直接使用 yfinance 原生下載
            df = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
            
            if df is None or df.empty:
                return None
                
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # 計算技術指標
            if len(df) >= 20:
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))
                df['MA20'] = df['Close'].rolling(window=20).mean()
            return df
            
        except Exception as e:
            if "Rate limited" in str(e) and attempt < max_retries - 1:
                time.sleep(5)  # 等待 5 秒後重試
                continue
            else:
                return None
    return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢"):
        with st.spinner("獲取資料中..."):
            data = fetch_data(ticker)
            if data is not None and 'Close' in data.columns:
                st.line_chart(data[['Close', 'MA20']])
            else:
                st.error("無法取得資料，請稍後再試或檢查代號。")

elif menu == "AI 選股與指標":
    if st.button("掃描清單"):
        results = []
        progress_bar = st.progress(0)
        tickers = ["2330.TW", "2454.TW"]
        
        for i, t in enumerate(tickers):
            df = fetch_data(t)
            if df is not None and 'RSI' in df.columns:
                results.append({"代號": t, "RSI": round(df['RSI'].iloc[-1], 2)})
            progress_bar.progress((i + 1) / len(tickers))
        
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.write("目前無可用的資料或已被限制，請稍候重試。")
