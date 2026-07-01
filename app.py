import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# --- 側邊欄：股票搜尋 ---
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)", value="2330")
search_button = st.sidebar.button("開始搜尋")

# --- 數據獲取函式 ---
@st.cache_data(ttl=3600)
def get_stock_data(ticker_symbol):
    """取得股票數據，加入快取避免頻繁請求"""
    try:
        # 加上 .TW 後綴
        ticker = yf.Ticker(f"{ticker_symbol}.TW")
        info = ticker.info
        hist = ticker.history(period="1mo")
        return info, hist
    except Exception as e:
        return None, None

# --- 主邏輯 ---
if search_button or ticker_input:
    with st.spinner(f"正在分析 {ticker_input}..."):
        info, hist = get_stock_data(ticker_input)
        
        if info and 'regularMarketPrice' in info:
            # 顯示指標
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"${info.get('regularMarketPrice', 0):,.2f}")
            col2.metric("本益比", info.get('trailingPE', 'N/A'))
            col3.metric("每股盈餘", info.get('trailingEps', 'N/A'))
            col4.metric("市值", f"{info.get('marketCap', 0) / 1e9:.2f} B")

            # 繪圖
            if hist is not None:
                st.subheader("近期走勢圖")
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name="收盤價")])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"已成功載入 {ticker_input} 的數據")
        else:
            st.error("無法取得該股票數據，請檢查代碼是否正確。")

else:
    st.info("請在側邊欄輸入代碼並按下「開始搜尋」。")
