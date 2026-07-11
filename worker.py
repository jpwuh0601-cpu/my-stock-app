import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 合併後的數據獲取邏輯 ---
def fetch_stock_data_local(ticker):
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or "currentPrice" not in info:
            return {"error": f"無法獲取 {ticker} 資料"}
        
        data = {
            "price": info.get("currentPrice", 0.0),
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "change": info.get("regularMarketChange", 0.0)
        }
        return data
    except Exception as e:
        return {"error": str(e)}

# --- UI 顯示 ---
st.set_page_config(page_title="專業股市儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

ticker = st.text_input("輸入股票代號", "2330")

if st.button("查詢分析"):
    with st.spinner("讀取中..."):
        data = fetch_stock_data_local(ticker)
        if "error" in data:
            st.error(data["error"])
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['price']:.2f}")
            col2.metric("每股淨值", f"{data['nav']:.2f}")
            col3.metric("本益比", f"{data['pe']:.2f}")
            col4.metric("EPS", f"{data['eps']:.2f}")
            
            st.success("數據載入成功！")
