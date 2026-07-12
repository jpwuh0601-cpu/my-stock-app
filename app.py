import streamlit as st
import os

# 1. 安全設定配置
try:
    st.set_page_config(page_title="股市儀表板", layout="wide")
except:
    pass

st.title("📈 專業股市決策儀表板")

# 2. 強制檢查套件環境
try:
    import yfinance as yf
    import pandas as pd
    st.success("環境套件載入成功！")
except ImportError as e:
    st.error(f"環境套件安裝缺失，請檢查 requirements.txt: {e}")
    st.stop()

# 3. 核心查詢功能
ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "").strip().upper()

if ticker_input:
    with st.spinner(f"正在查詢 {ticker_input}..."):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            
            if "currentPrice" not in info:
                st.error("無法找到該股票代號，請確認代號是否正確。")
            else:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("股價", info.get("currentPrice", 0))
                col2.metric("每股淨值", info.get("bookValue", 0))
                col3.metric("本益比", info.get("trailingPE", 0))
                col4.metric("EPS", info.get("trailingEps", 0))
        except Exception as e:
            st.error(f"資料錯誤: {e}")
