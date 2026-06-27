import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    """加入隨機延遲與更謹慎的下載機制"""
    # 隨機延遲，避免伺服器判定為機器人攻擊
    time.sleep(random.uniform(2, 5))
    
    try:
        # 使用 proxy 參數（雖然不一定能用，但 yfinance 在雲端環境下偶爾需要這樣觸發）
        # 增加 user-agent 設定，讓請求更像真實瀏覽器
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        df = yf.download(ticker, period="6mo", progress=False, auto_adjust=True, threads=False)
        
        if df is None or df.empty:
            return None
        
        # 處理 MultiIndex
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
            
    except Exception:
        return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢"):
        data = fetch_data(ticker)
        if data is not None and 'Close' in data.columns:
            st.line_chart(data[['Close', 'MA20']])
        else:
            st.error("下載失敗，可能被頻率限制，請稍候再試。")

elif menu == "AI 選股與指標":
    if st.button("掃描清單"):
        results = []
        tickers = ["2330.TW", "2454.TW", "2317.TW", "3008.TW"]
        progress_bar = st.progress(0)
        
        for i, t in enumerate(tickers):
            df = fetch_data(t)
            if df is not None and 'RSI' in df.columns:
                results.append({"代號": t, "RSI": round(df['RSI'].iloc[-1], 2)})
            progress_bar.progress((i + 1) / len(tickers))
        
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.warning("掃描中斷或無資料，請等待數分鐘後再試。")
