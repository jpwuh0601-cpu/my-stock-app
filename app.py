import streamlit as st
import yfinance as yf
import pandas as pd
import requests

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (輕量版)", layout="wide")
st.title("📊 專業股市決策系統 (輕量穩定版)")

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

# 定義抓取資料函式 (大幅精簡，直接透過 yfinance 預設存取)
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    try:
        # 使用極簡化存取，不強加 session 模擬，避免 session 初始化卡住
        stock = yf.Ticker(ticker)
        # 獲取最近 5 天資料即可，避免抓取過多歷史導致請求超時
        df = stock.history(period="5d") 
        if not df.empty:
            return df.sort_index(ascending=False)
        else:
            return "empty"
    except Exception as e:
        return str(e)

if menu == "個股分析":
    st.info("提示：輸入代號 (例如 2330.TW, AAPL)")
    ticker_input = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("正在讀取..."):
            result = fetch_stock_data(ticker_input.strip().upper())
            if isinstance(result, pd.DataFrame):
                current_price = float(result['Close'].iloc[0])
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                st.table(result.head(5))
            elif result == "empty":
                st.error("系統讀取超時或找不到代號，請重新整理頁面。")
            else:
                st.error(f"系統錯誤: {result}")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, AAPL")
    if st.button("開始比較"):
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        data = []
        for t in tickers:
            result = fetch_stock_data(t)
            if isinstance(result, pd.DataFrame):
                data.append({"代號": t, "最新價": round(float(result['Close'].iloc[0]), 2)})
            else:
                data.append({"代號": t, "最新價": "抓取失敗"})
        if data:
            st.table(pd.DataFrame(data))
