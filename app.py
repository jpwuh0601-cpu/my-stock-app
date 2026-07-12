import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 自動處理代號格式的函數
def get_clean_ticker(ticker):
    ticker = ticker.strip()
    if ticker.isdigit():
        # 自動判斷上市或上櫃 (預設加 .TW，若需上櫃需自行調整或增加判斷)
        return f"{ticker}.TW"
    return ticker

# 資料查詢與渲染
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析"):
    target_ticker = get_clean_ticker(ticker_input)
    st.session_state['ticker'] = target_ticker

if 'ticker' in st.session_state:
    target = st.session_state['ticker']
    try:
        stock = yf.Ticker(target)
        info = stock.info
        
        if not info or 'currentPrice' not in info:
            st.error(f"無法查詢代號 {target}，請確認是否為有效台股代號。")
        else:
            # 顯示報價
            price = info.get('currentPrice', 0)
            change = info.get('regularMarketChange', 0)
            color = "red" if change >= 0 else "green"
            st.markdown(f"### 即時股價: {price} <span style='color:{color}'>({'▲' if change>=0 else '▼'} {abs(change)} 元)</span>", unsafe_allow_html=True)
            
            # 其他指標顯示...
            st.success(f"已成功載入 {target} 的數據")
            
    except Exception as e:
        st.error(f"查詢發生錯誤: {str(e)}")
