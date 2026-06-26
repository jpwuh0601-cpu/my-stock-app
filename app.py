import streamlit as st
from analysis_utils import get_stock_analysis

st.title("股票即時分析器")
ticker = st.text_input("請輸入股票代碼 (例如 2330.TW)", "2330.TW")

if st.button("開始分析"):
    price, sma, status = get_stock_analysis(ticker)
    if price:
        st.write(f"### 最新價格: {price:.2f}")
        st.write(f"### 20日均線: {sma:.2f}")
        st.write(f"### 市場狀態: {status}")
    else:
        st.error("無法取得該股票資料，請檢查代碼。")
