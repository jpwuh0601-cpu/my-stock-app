import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

# 設定網頁標題
st.set_page_config(page_title="專業股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 優化連線：建立帶有緩存與限流的 Session
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND * 5)),
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

# 定義功能模組
def get_technical_indicators(df):
    """純 Python 計算技術指標 (RSI, MA)"""
    delta = df['收盤價'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['MA20'] = df['收盤價'].rolling(window=20).mean()
    return df

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        # 使用自定義 session 增加穩定度
        ticker_data = yf.Ticker(ticker, session=session)
        df = ticker_data.history(period="6mo")
        
        if not df.empty:
            df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
            return get_technical_indicators(df.sort_index())
        return None
    except Exception as e:
        st.error(f"連線錯誤: {e}")
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
            st.metric("最新收盤價", f"{round(data['收盤價'].iloc[-1], 2)}")
            st.line_chart(data[['收盤價', 'MA20']])
        else:
            st.warning("無法獲取資料，請確認代號是否正確。")

elif menu == "AI 選股與指標":
    st.subheader("🤖 AI 自動化選股系統")
    if st.button("執行全市場掃描 (測試代號)"):
        target_tickers = ["2330.TW", "2454.TW"]
        results = []
        for t in target_tickers:
            df = fetch_data(t)
            if df is not None and df['RSI'].iloc[-1] < 30:
                results.append({"代號": t, "當前RSI": round(df['RSI'].iloc[-1], 2), "狀態": "超賣"})
        st.table(pd.DataFrame(results) if results else "無符合條件個股")

elif menu == "黑天鵝警示系統":
    st.warning("⚠️ 黑天鵝監控中心")
    target_ticker = st.text_input("監控代號", "2330.TW")
    notify_token = st.text_input("LINE Notify Token", type="password")
    
    if st.button("啟動自動監控"):
        data = fetch_data(target_ticker)
        if data is not None and data['RSI'].iloc[-1] < 30:
            msg = f"警示：{target_ticker} 超賣 (RSI: {round(data['RSI'].iloc[-1], 2)})"
            if notify_token:
                send_line_notify(notify_token, msg)
                st.success("通知已發送")

elif menu == "LINE 通知與 Bot 設定":
    st.subheader("📱 LINE 服務整合設定")
    st.info("此系統已優化連線穩定度。")
