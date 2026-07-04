import streamlit as st
import os
import json

st.write("系統正在初始化...")

# 測試 JSON 是否存在
if os.path.exists("market_data.json"):
    st.write("偵測到市場數據檔")
else:
    st.write("錯誤：找不到 market_data.json，請確認 Action 是否執行完成")
import streamlit as st
import yfinance as yf
import requests
import os
import json
import plotly.express as px
import pandas as pd

# --- 1. 資料讀取 ---
def get_stock_metrics(ticker_symbol):
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(ticker_symbol, {})
    return {}

# --- 2. 頁面設定 ---
st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)")

if input_ticker:
    ticker = yf.Ticker(input_ticker)
    info = ticker.info
    metrics = get_stock_metrics(input_ticker)
    
    if "currentPrice" in info:
        # A. 視覺化圖表：歷史走勢
        st.subheader("📈 近期走勢互動圖表")
        hist = ticker.history(period="1mo")
        fig = px.line(hist, y="Close", title=f"{input_ticker} 近期股價走勢")
        st.plotly_chart(fig, use_container_width=True)
        
        # B. 財務指標矩陣
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨額", f"{info.get('bookValue', 0):.2f}")
        col2.metric("本益比", f"{info.get('forwardPE', 0):.2f}")
        col3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
        
        # C. AI 顧問報告
        st.subheader("🤖 AI 顧問深度分析")
        st.info(metrics.get('ai_insight', "正在分析中..."))
        
        # D. 風險狀態
        st.warning(f"監控狀態: {metrics.get('black_swan', '安全')}")
    else:
        st.error("查無資料，請確認代號。")
