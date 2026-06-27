import streamlit as st
import twstock
import pandas as pd
import time
import random
import requests
import matplotlib.pyplot as plt
import io

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業台股 AI 決策系統 (含趨勢圖表通知)")

# 產業與代號映射表
SECTOR_MAP = {
    "半導體": ["2330", "2454", "2303", "3034", "6669"],
    "金融股": ["2881", "2882", "2886", "2891"],
    "營建股": ["2548", "2504", "5522"],
    "航運股": ["2603", "2609", "2615"]
}

# 獲取三大法人數據
def fetch_chips(ticker):
    try:
        url = f"https://www.twse.com.tw/fund/T86?response=json&selectType=00&stockNo={ticker}"
        res = requests.get(url, timeout=5)
        data = res.json()
        if 'data' in data:
            return pd.DataFrame(data['data'], columns=data['fields']).tail(1)
        return None
    except:
        return None

# 發送帶有圖表的 LINE 通知
def send_line_notify_with_chart(token, message, df):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 繪製圖表
    plt.figure(figsize=(10, 5))
    plt.plot(df.index[-30:], df['MACD'].iloc[-30:], label='MACD')
    plt.plot(df.index[-30:], df['Signal'].iloc[-30:], label='Signal')
    plt.title("Recent MACD Trend")
    plt.legend()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    
    payload = {"message": message}
    files = {"imageFile": img_buf}
    requests.post(url, headers=headers, data=payload, files=files)

# MACD 簡易回測邏輯
def perform_backtest(df):
    df['Signal_Cross'] = (df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))
    returns = []
    for i in range(len(df)):
        if df['Signal_Cross'].iloc[i] and i + 5 < len(df):
            ret = (df['Close'].iloc[i+5] - df['Close'].iloc[i]) / df['Close'].iloc[i]
            returns.append(ret)
    return round(sum(returns) / len(returns) * 100, 2) if returns else 0.0

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    time.sleep(random.uniform(0.5, 1.0))
    try:
        stock = twstock.Stock(ticker)
        data = stock.fetch_from(2026, 1) 
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df.rename(columns={'close': 'Close'}, inplace=True)
        
        if len(df) >= 26:
            delta = df['Close'].diff()
            df['RSI'] = 100 - (100 / (1 + (delta.where(delta > 0, 0).rolling(14).mean() / (-delta.where(delta < 0, 0).rolling(14).mean()))))
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df
    except:
        return None

# 介面
menu = st.sidebar.radio("AI 決策核心", ["個股儀表板", "產業選股矩陣", "LINE 通知設定"])
token = st.secrets.get("LINE_NOTIFY_TOKEN")

if menu == "個股儀表板":
    ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
    if st.button("查詢"):
        data = fetch_data(ticker)
        chips = fetch_chips(ticker)
        if data is not None:
            st.subheader(f"{ticker} 技術指標")
            st.line_chart(data[['Close', 'MA20']])
            # 發送測試圖表通知
            if st.button("發送測試通知至 LINE"):
                if token:
                    send_line_notify_with_chart(token, f"測試報告: {ticker} 最新 MACD 趨勢", data)
                    st.success("通知已送出")
                else:
                    st.error("請先設定 Token")
        else:
            st.error("資料獲取失敗。")

elif menu == "產業選股矩陣":
    sector = st.selectbox("選擇產業類別", list(SECTOR_MAP.keys()))
    if st.button("開始產業掃描"):
        results = []
        for t in SECTOR_MAP[sector]:
            df = fetch_data(t)
            if df is not None:
                win_rate = perform_backtest(df)
                results.append({
                    "代號": t, 
                    "RSI": round(df['RSI'].iloc[-1], 2),
                    "回測參考(5日平均績效%)": win_rate
                })
        st.table(pd.DataFrame(results))

elif menu == "LINE 通知設定":
    st.header("系統提示")
    st.write("請確保已在 Streamlit Secrets 設定 LINE_NOTIFY_TOKEN。")
