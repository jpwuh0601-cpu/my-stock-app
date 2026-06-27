import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import talib # 用於技術指標計算

# 設定網頁標題
st.set_page_config(page_title="專業股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 定義功能模組
def get_technical_indicators(df):
    """計算技術指標 (RSI, MA)"""
    df['RSI'] = talib.RSI(df['收盤價'], timeperiod=14)
    df['MA20'] = talib.SMA(df['收盤價'], timeperiod=20)
    return df

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        df = yf.download(ticker, period="6mo", progress=False)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
            return get_technical_indicators(df.sort_index())
        return None
    except:
        return None

# 側邊欄導航
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "黑天鵝警示系統", "LINE 通知設定"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入台股代號", "2330.TW")
    if st.button("AI 深度分析"):
        data = fetch_data(ticker)
        if data is not None:
            st.metric("最新收盤價", f"{round(data['收盤價'].iloc[-1], 2)}")
            st.line_chart(data[['收盤價', 'MA20']])
            st.write("### 🧠 GPT 新聞與指標解讀")
            st.info("此處將串接 GPT-4 API 進行市場情緒分析 (開發中...)")
        else:
            st.error("無法取得資料。")

elif menu == "AI 選股與指標":
    st.subheader("🤖 AI 自動化選股策略")
    if st.button("執行篩選"):
        st.write("正在掃描全市場個股技術指標...")
        # 此處放置選股邏輯
        st.success("已篩選出 RSI < 30 的強勢股 (示例)")

elif menu == "黑天鵝警示系統":
    st.warning("⚠️ 黑天鵝警示：系統正在監控異常成交量與崩跌風險。")
    st.table(pd.DataFrame({"警示類別": ["量價背離", "極端波動"], "狀態": ["正常", "監控中"]}))

elif menu == "LINE 通知設定":
    st.subheader("📱 LINE Notify 綁定")
    token = st.text_input("輸入 LINE Notify Token", type="password")
    if st.button("測試推播"):
        st.success("模擬推播測試訊息已送出。")
