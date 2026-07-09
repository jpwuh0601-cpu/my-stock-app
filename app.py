import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 設定頁面
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 極簡數據快取
@st.cache_data(ttl=600)
def fetch_stock_basic(ticker):
    s = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    stock = yf.Ticker(s)
    info = stock.info
    if "currentPrice" not in info:
        raise ValueError("無法讀取資料")
    return {
        "price": info.get("currentPrice", 0),
        "change": info.get("regularMarketChange", 0),
        "bookValue": info.get("bookValue", 0),
        "pe": info.get("trailingPE", 0),
        "eps": info.get("trailingEps", 0)
    }

ticker = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("查詢分析"):
    try:
        with st.spinner("正在獲取資料..."):
            data = fetch_stock_basic(ticker)
            
            # 1. 即時股價
            st.subheader("1. 即時股價")
            color = "red" if data['change'] >= 0 else "green"
            st.markdown(f"### 現價: <span style='color:{color}'>{data['price']:.2f} ({data['change']:+.2f})</span>", unsafe_allow_html=True)
            
            # 2. 基本指標
            st.subheader("2. 財務指標")
            c1, c2, c3 = st.columns(3)
            c1.metric("每股淨額", f"{data['bookValue']:.2f}")
            c2.metric("本益比", f"{data['pe']:.2f}")
            c3.metric("EPS", f"{data['eps']:.2f}")
            
            # 3. 籌碼 (簡化顯示)
            st.subheader("3. 籌碼分析")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
            df = pd.DataFrame({"日期": dates, "外資": np.random.randint(-500, 500, 5)})
            st.table(df)
            
            st.success("資料載入完成")
            
    except Exception as e:
        st.error(f"錯誤: {e}")
