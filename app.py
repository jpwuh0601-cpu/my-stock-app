import streamlit as st
import yfinance as yf
import pandas as pd
import requests

# 設定網頁標題
st.set_page_config(page_title="專業股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 定義技術指標計算
def get_technical_indicators(df):
    if len(df) < 20:
        return df
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['MA20'] = df['Close'].rolling(window=20).mean()
    return df

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        df = yf.download(ticker, period="6mo", progress=False)
        if df is None or df.empty:
            return None
        # 處理 yfinance 可能回傳的多層索引 (MultiIndex)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # 確保有需要的欄位
        if 'Close' not in df.columns:
            return None
            
        df = get_technical_indicators(df)
        return df
    except Exception:
        return None

# 側邊欄導航
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "黑天鵝警示系統"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入台股代號", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("獲取數據中..."):
            data = fetch_data(ticker)
            if data is not None and not data.empty:
                st.metric("最新收盤價", f"{round(data['Close'].iloc[-1], 2)}")
                st.line_chart(data[['Close', 'MA20']])
            else:
                st.error("無法獲取該代號資料。")

elif menu == "AI 選股與指標":
    st.subheader("🤖 AI 自動化選股系統")
    if st.button("執行全市場掃描"):
        target_tickers = ["2330.TW", "2454.TW", "2317.TW", "3008.TW"]
        results = []
        with st.spinner("掃描中..."):
            for t in target_tickers:
                df = fetch_data(t)
                if df is not None and 'RSI' in df.columns:
                    rsi_val = df['RSI'].iloc[-1]
                    if rsi_val < 30:
                        results.append({"代號": t, "當前RSI": round(float(rsi_val), 2), "狀態": "超賣"})
        
        # 這裡嚴格確保只有在有資料時才建立 DataFrame
        if len(results) > 0:
            df_results = pd.DataFrame(results)
            st.table(df_results)
        else:
            st.info("目前無符合條件的超賣個股。")

elif menu == "黑天鵝警示系統":
    st.warning("⚠️ 黑天鵝監控中心")
    st.write("此模組可整合 LINE Notify 進行自動化提醒。")
