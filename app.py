import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
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
    """使用 yfinance 下載資料，不使用自定義 session 以避免衝突"""
    try:
        # 官方推薦用法
        df = yf.download(ticker, period="6mo", progress=False)
        if not df.empty:
            # yfinance 回傳的多層 index 處理
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = get_technical_indicators(df)
            return df
        return None
    except Exception as e:
        st.error(f"資料獲取失敗: {e}")
        return None

def send_line_notify(token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    return requests.post(url, headers=headers, data=payload)

# 側邊欄導航
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "黑天鵝警示系統", "LINE 通知與 Bot 設定"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入台股代號", "2330.TW")
    if st.button("查詢分析"):
        data = fetch_data(ticker)
        if data is not None:
            st.metric("最新收盤價", f"{round(data['Close'].iloc[-1], 2)}")
            st.line_chart(data[['Close', 'MA20']])
        else:
            st.warning("無法獲取資料，請確認代號是否正確。")

elif menu == "AI 選股與指標":
    st.subheader("🤖 AI 自動化選股系統")
    if st.button("執行全市場掃描"):
        target_tickers = ["2330.TW", "2454.TW", "2317.TW", "3008.TW"]
        results = []
        with st.spinner("正在聯網掃描..."):
            for t in target_tickers:
                df = fetch_data(t)
                if df is not None and not df.empty and 'RSI' in df.columns:
                    rsi_val = df['RSI'].iloc[-1]
                    if rsi_val < 30:
                        results.append({"代號": t, "當前RSI": round(rsi_val, 2), "狀態": "超賣"})
        
        if results:
            st.table(pd.DataFrame(results))
        else:
            st.info("目前無符合條件的超賣個股。")

elif menu == "黑天鵝警示系統":
    st.warning("⚠️ 黑天鵝監控中心")
    target_ticker = st.text_input("監控代號", "2330.TW")
    notify_token = st.text_input("LINE Notify Token", type="password")
    
    if st.button("啟動自動監控"):
        data = fetch_data(target_ticker)
        if data is not None and 'RSI' in data.columns and data['RSI'].iloc[-1] < 30:
            msg = f"警示：{target_ticker} 超賣 (RSI: {round(data['RSI'].iloc[-1], 2)})"
            if notify_token:
                send_line_notify(notify_token, msg)
                st.success("通知已發送")
