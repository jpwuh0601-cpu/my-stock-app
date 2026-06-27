import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統 (MACD 優化版)")

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    """加入隨機延遲與 MACD 計算"""
    time.sleep(random.uniform(2, 5))
    
    try:
        df = yf.download(ticker, period="6mo", progress=False, auto_adjust=True, threads=False)
        
        if df is None or df.empty:
            return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # 計算技術指標
        if len(df) >= 26:
            # RSI & MA20
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df['MA20'] = df['Close'].rolling(window=20).mean()
            
            # MACD 計算
            ema12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema12 - ema26
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            
        return df
            
    except Exception:
        return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢"):
        data = fetch_data(ticker)
        if data is not None and 'Close' in data.columns:
            st.subheader(f"{ticker} 技術指標走勢")
            # 顯示收盤價與移動平均
            st.line_chart(data[['Close', 'MA20']])
            # 顯示 MACD 與 Signal
            st.write("MACD 指標分析")
            st.line_chart(data[['MACD', 'Signal']])
        else:
            st.error("下載失敗，請稍候再試。")

elif menu == "AI 選股與指標":
    if st.button("掃描清單"):
        results = []
        tickers = ["2330.TW", "2454.TW", "2317.TW", "3008.TW"]
        progress_bar = st.progress(0)
        
        for i, t in enumerate(tickers):
            df = fetch_data(t)
            if df is not None and 'MACD' in df.columns:
                # 簡單邏輯：MACD > Signal 為強勢
                status = "多頭趨勢" if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else "弱勢盤整"
                results.append({
                    "代號": t, 
                    "RSI": round(df['RSI'].iloc[-1], 2),
                    "MACD": round(df['MACD'].iloc[-1], 2),
                    "趨勢": status
                })
            progress_bar.progress((i + 1) / len(tickers))
        
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.warning("掃描中斷或無資料。")
