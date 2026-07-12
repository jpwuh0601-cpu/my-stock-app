import streamlit as st
import yfinance as yf

# 為了徹底避開舊的快取衝突，我們將快取函數名稱更改並重新定義
@st.cache_data(ttl=600)
def fetch_stock_info(ticker):
    # 此函式只接受一個參數 'ticker'
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

st.title("股票分析器")
ticker_input = st.text_input("輸入代號", "2330.TW")

if st.button("查詢"):
    # 呼叫新的函數名稱以確保避開舊有快取記憶
    data = fetch_stock_info(ticker_input)
    st.write(data.get("currentPrice", "讀取中..."))
