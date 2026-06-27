import streamlit as st
import twstock
import pandas as pd
import time
import random
import requests

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業台股 AI 決策系統 (含 LINE 通知)")

# LINE Notify 推送函數
def send_line_notify(token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    """使用 twstock 獲取資料並計算指標"""
    time.sleep(random.uniform(1, 2))
    
    try:
        code = ticker.replace(".TW", "")
        stock = twstock.Stock(code)
        data = stock.fetch_from(2026, 1) 
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df.rename(columns={'close': 'Close'}, inplace=True)
        
        if df is None or df.empty:
            return None
            
        if len(df) >= 26:
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df['MA20'] = df['Close'].rolling(window=20).mean()
            
            ema12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema12 - ema26
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            
        return df
    except Exception:
        return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "LINE 通知與 Bot 設定"])

if menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
    if st.button("查詢"):
        data = fetch_data(ticker)
        if data is not None and 'Close' in data.columns:
            st.subheader(f"{ticker} 技術指標走勢")
            st.line_chart(data[['Close', 'MA20']])
            st.write("MACD 指標分析")
            st.line_chart(data[['MACD', 'Signal']])
        else:
            st.error("下載失敗，請檢查代號或稍候再試。")

elif menu == "AI 選股與指標":
    token = st.sidebar.text_input("輸入 LINE Notify Token", type="password")
    if st.button("掃描清單"):
        results = []
        tickers = ["2330", "2454", "2317", "3008"]
        progress_bar = st.progress(0)
        
        for i, t in enumerate(tickers):
            df = fetch_data(t)
            if df is not None and 'MACD' in df.columns:
                rsi = round(df['RSI'].iloc[-1], 2)
                status = "多頭趨勢" if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else "弱勢盤整"
                results.append({
                    "代號": t, 
                    "RSI": rsi,
                    "MACD": round(df['MACD'].iloc[-1], 2),
                    "趨勢": status
                })
                # 黑天鵝警示邏輯：RSI < 30
                if rsi < 30 and token:
                    send_line_notify(token, f"【黑天鵝警示】股票 {t} RSI 過低 ({rsi})，請留意風險！")
            
            progress_bar.progress((i + 1) / len(tickers))
        
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.warning("掃描中斷或無資料。")

elif menu == "LINE 通知與 Bot 設定":
    st.header("LINE Notify 設定")
    st.write("請至 [LINE Notify](https://notify-bot.line.me/) 申請 Token，並將其貼入「AI 選股與指標」頁面的設定欄位中。")
