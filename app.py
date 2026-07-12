import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 設定頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 清除所有殘留快取，確保函數定義是新的
@st.cache_data(ttl=300)
def get_data_cached(ticker):
    # 統一使用 ticker 作為變數名稱
    clean_ticker = ticker if (ticker.endswith(".TW") or ticker.endswith(".TWO")) else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        data = {
            "currentPrice": info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
            "regularMarketChangePercent": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0)
        }
        return data, False, clean_ticker
    except Exception as e:
        return {"error": str(e)}, True, clean_ticker

# 顯示標題
st.title("📈 專業股市決策儀表板")

# 使用者輸入
ticker_input = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        # 呼叫時明確傳遞變數
        data, is_error, used_ticker = get_data_cached(ticker_input)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 資料: {data.get('error')}")
        else:
            st.markdown(f"### {used_ticker} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChangePercent']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")
            st.success("數據讀取成功！")
