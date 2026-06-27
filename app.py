# app.py
import streamlit as st
from analysis_utils import get_stock_analysis

st.set_page_config(page_title="專業股市儀表板", layout="wide")
st.title("📊 專業股市儀表板")

@st.cache_data(ttl=3600)
def cached_analysis(ticker):
    return get_stock_analysis(ticker)

ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")

if st.button("查詢分析"):
    price, sma, status, data = cached_analysis(ticker)
    
    if price:
        # 第一行數據
        col1, col2, col3 = st.columns(3)
        col1.metric("即時報價", f"{data['現價']:.2f}")
        col2.metric("漲跌幅", data['漲跌幅'])
        col3.metric("EPS", data['EPS'])
        
        # 第二行數據
        col4, col5, col6 = st.columns(3)
        col4.metric("本益比", data['本益比'])
        col5.metric("每股淨值", data['每股淨值'])
        col6.metric("發行股數", f"{data['發行股數']:,}")
        
        st.divider()
        st.write(f"### 趨勢狀態: {status} (20日均線: {sma:.2f})")
    else:
        st.error("無法取得資料")
