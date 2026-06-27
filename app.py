import streamlit as st
import yfinance as yf
import pandas as pd

# 基礎設定
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 強制關閉 yfinance 的任何快取行為
yf.pdr_override() 

@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        # 使用最基礎的下載方式，並確保不使用任何 session 快取
        # auto_adjust=True 讓 yfinance 自動處理分割權益，降低處理複雜度
        df = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
        
        if df is None or df.empty:
            return None
            
        # 處理 MultiIndex 問題 (部分 yfinance 版本會出現)
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
    except Exception as e:
        # 將錯誤顯示在頁面上以利偵錯
        st.error(f"下載失敗: {e}")
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
            st.error("無法取得有效資料，請檢查代號是否正確。")

elif menu == "AI 選股與指標":
    if st.button("掃描清單"):
        results = []
        for t in ["2330.TW", "2454.TW"]:
            df = fetch_data(t)
            if df is not None and 'RSI' in df.columns:
                results.append({"代號": t, "RSI": round(df['RSI'].iloc[-1], 2)})
        
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.write("掃描失敗或無資料。")
