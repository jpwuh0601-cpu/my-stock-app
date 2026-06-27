import streamlit as st
import twstock
import pandas as pd
import time
import random
import requests

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業台股 AI 決策系統 (含籌碼分析)")

# 獲取三大法人數據 (爬取證交所公開資料)
def fetch_chips(ticker):
    try:
        # 證交所三大法人 API
        url = f"https://www.twse.com.tw/fund/T86?response=json&selectType=00&stockNo={ticker.replace('.TW', '')}"
        res = requests.get(url, timeout=5)
        data = res.json()
        if 'data' in data:
            df = pd.DataFrame(data['data'], columns=data['fields'])
            # 簡化回傳最後一筆紀錄
            return df.tail(1)
        return None
    except:
        return None

# LINE Notify 推送函數
def send_line_notify(token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    time.sleep(random.uniform(1, 2))
    try:
        code = ticker.replace(".TW", "")
        stock = twstock.Stock(code)
        data = stock.fetch_from(2026, 1) 
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df.rename(columns={'close': 'Close'}, inplace=True)
        
        if len(df) >= 26:
            # 技術指標計算
            delta = df['Close'].diff()
            df['RSI'] = 100 - (100 / (1 + (delta.where(delta > 0, 0).rolling(14).mean() / (-delta.where(delta < 0, 0).rolling(14).mean()))))
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df
    except:
        return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "AI 選股與指標", "LINE 通知與 Bot 設定"])
token = st.secrets.get("LINE_NOTIFY_TOKEN")

if menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
    if st.button("查詢"):
        # 獲取價格與籌碼
        data = fetch_data(ticker)
        chips = fetch_chips(ticker)
        
        if data is not None:
            st.subheader(f"{ticker} 技術指標")
            st.line_chart(data[['Close', 'MA20']])
            
            if chips is not None:
                st.subheader("籌碼面統計 (三大法人)")
                st.dataframe(chips)
        else:
            st.error("資料獲取失敗。")

elif menu == "AI 選股與指標":
    if st.button("掃描清單"):
        tickers = ["2330", "2454", "2317", "3008"]
        for t in tickers:
            df = fetch_data(t)
            if df is not None:
                st.write(f"代號: {t} | RSI: {round(df['RSI'].iloc[-1], 2)} | MACD 狀態: {'強勢' if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else '弱勢'}")
