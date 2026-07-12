import streamlit as st
import yfinance as yf

# 清除舊的快取影響，確保名稱完全對應
@st.cache_data(ttl=600)
def get_data_cached(ticker):
    # 此函式只接受一個參數 'ticker'
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

st.title("股票分析器")
ticker_input = st.text_input("輸入代號", "2330.TW")

if st.button("查詢"):
    # 這裡只傳遞一個參數，與上方定義對應
    data = get_data_cached(ticker_input)
    st.write(data.get("currentPrice", "讀取中..."))
