import streamlit as st
import yfinance as yf
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (Yahoo Finance 強制版)", layout="wide")
st.title("📊 專業股市決策系統 (Yahoo Finance 強制版)")

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

# 定義抓取資料函式
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    try:
        # 關鍵修正：透過 session 強制模擬瀏覽器行為，避開網路封鎖
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        stock = yf.Ticker(ticker, session=session)
        # 嘗試抓取資料
        df = stock.history(period="1mo") 
        if not df.empty:
            return df.sort_index(ascending=False)
        else:
            return "empty"
    except Exception as e:
        return str(e)

# 引入 requests 以支援 session 模式
import requests

if menu == "個股分析":
    st.info("提示：輸入代號查詢 (台股請加 .TW，美股直接輸入，例如: 2330.TW, AAPL)")
    ticker_input = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("正在強制抓取資料..."):
            result = fetch_stock_data(ticker_input.strip().upper())
            if isinstance(result, pd.DataFrame):
                current_price = float(result['Close'].iloc[0])
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                st.table(result.head(5))
            elif result == "empty":
                st.error("查無資料，可能是該代號無歷史數據，或連線依然受限。")
            else:
                st.error(f"連線失敗: {result}")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW, AAPL")
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
