import streamlit as st
import yfinance as yf
import json
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 設定頁面配置，提高效能與互動性
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

@st.cache_data(ttl=600)
def fetch_live_data(ticker_code):
    """手動觸發的數據更新功能，避免啟動時卡死"""
    try:
        ticker = yf.Ticker(f"{ticker_code}.TW")
        info = ticker.info
        hist = ticker.history(period="1mo")
        return info, hist
    except Exception as e:
        return None, f"獲取失敗: {str(e)}"

def load_local_data():
    """優先讀取離線檔案，確保頁面載入速度"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

ticker_input = st.sidebar.text_input("輸入台股代碼 (預設 2330)", value="2330")

# 區分：本地預覽與即時獲取
if st.sidebar.button("載入本地數據"):
    data = load_local_data()
    if data:
        st.subheader("離線數據快照")
        st.json(data)
    else:
        st.warning("找不到本地數據檔案，請先執行 worker.py。")

if st.sidebar.button("獲取即時數據 (線上)"):
    with st.spinner("正在連接 Yahoo Finance 獲取數據..."):
        info, hist = fetch_live_data(ticker_input)
        if info and not isinstance(info, str):
            st.success("數據獲取成功！")
            col1, col2, col3 = st.columns(3)
            col1.metric("目前價格", f"{info.get('currentPrice', 'N/A')} TWD")
            col2.metric("本益比", info.get("trailingPE", "N/A"))
            col3.metric("市值", f"{info.get('marketCap', 0) / 1e9:.2f} B")
            
            if hist is not None and not hist.empty:
                fig = go.Figure(data=go.Scatter(x=hist.index, y=hist['Close'], mode='lines'))
                fig.update_layout(title="近一個月股價趨勢")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"無法獲取數據：{info}")

st.info("💡 提示：為了避免頁面卡死，請使用側邊欄按鈕手動載入數據。")
