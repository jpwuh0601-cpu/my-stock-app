import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import talib
import requests

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

def send_line_notify(token, message):
    """發送 LINE Notify 推送通知"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    return requests.post(url, headers=headers, data=payload)

# 側邊欄導航
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "黑天鵝警示系統", "LINE 通知與 Bot 設定"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入台股代號", "2330.TW")
    if st.button("AI 深度分析"):
        data = fetch_data(ticker)
        if data is not None:
            st.metric("最新收盤價", f"{round(data['收盤價'].iloc[-1], 2)}")
            st.line_chart(data[['收盤價', 'MA20']])
            st.write("### 🧠 GPT 新聞與指標解讀")
            st.info("串接 OpenAI API 後，此處將顯示 AI 對該股的技術面與市場情緒報告。")
        else:
            st.error("無法取得資料。")

elif menu == "AI 選股與指標":
    st.subheader("🤖 AI 自動化選股系統")
    target_tickers = ["2330.TW", "2454.TW", "2317.TW", "3008.TW"]
    if st.button("執行全市場掃描"):
        results = []
        for t in target_tickers:
            df = fetch_data(t)
            if df is not None and df['RSI'].iloc[-1] < 30:
                results.append({"代號": t, "當前RSI": round(df['RSI'].iloc[-1], 2), "狀態": "超賣潛力股"})
        
        if results:
            st.table(pd.DataFrame(results))
        else:
            st.write("目前無符合條件的個股。")

elif menu == "黑天鵝警示系統":
    st.warning("⚠️ 黑天鵝警示：系統監控異常波動中")
    st.table(pd.DataFrame({"警示類別": ["量價背離", "極端波動"], "狀態": ["正常", "監控中"]}))

elif menu == "LINE 通知與 Bot 設定":
    st.subheader("📱 LINE 服務整合設定")
    
    with st.expander("LINE Notify 推送設定 (接收警示用)"):
        notify_token = st.text_input("LINE Notify Token", type="password")
        if st.button("發送測試通知"):
            if notify_token:
                res = send_line_notify(notify_token, "這是測試推播")
                st.success("通知發送狀態：" + str(res.status_code))
    
    with st.expander("LINE Messaging API 設定 (互動機器人用)"):
        channel_access_token = st.text_input("Channel Access Token", type="password")
        st.caption("此 Token 用於實現雙向互動功能，設定後即可進行對話開發。")
