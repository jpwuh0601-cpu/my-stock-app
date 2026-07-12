import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

@st.cache_data(ttl=60)
def get_data_reliable(ticker):
    # 統一代號格式
    clean_ticker = ticker.strip().split('.')[0]
    full_ticker = f"{clean_ticker}.TW"
    
    # 嘗試抓取邏輯
    try:
        # 使用 yfinance 抓取
        stock = yf.Ticker(full_ticker)
        info = stock.info
        
        # 檢查是否讀取到數據
        if "currentPrice" not in info or info["currentPrice"] is None:
            return {"error": "找不到此股票代號，請檢查輸入是否正確。"}, True, full_ticker
            
        return {
            "currentPrice": info.get("currentPrice", 0.0),
            "regularMarketChange": info.get("regularMarketChange", 0.0),
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0)
        }, False, full_ticker
    except Exception as e:
        return {"error": f"系統錯誤: {str(e)}"}, True, full_ticker

ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在聯網讀取數據..."):
        data, is_error, used_ticker = get_data_reliable(ticker)
        
        if is_error:
            st.error(f"⚠️ {data['error']}")
        else:
            st.markdown(f"### {used_ticker} 即時資訊")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("即時股價", f"{data['currentPrice']:.2f}")
            c2.metric("每股淨值", f"{data['bookValue']:.2f}")
            c3.metric("本益比", f"{data['trailingPE']:.2f}")
            c4.metric("EPS", f"{data['trailingEps']:.2f}")
            st.success("數據讀取成功！")
