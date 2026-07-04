import streamlit as st
import yfinance as yf
import requests
import os
import json
import plotly.express as px
import pandas as pd

# --- 設定頁面 ---
st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# --- 核心數據載入函式 (加入容錯) ---
def get_stock_metrics(ticker_symbol):
    if not os.path.exists("market_data.json"):
        st.error("系統數據檔案不存在，請確認 GitHub Actions 是否完成執行。")
        return None
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(ticker_symbol)
    except Exception as e:
        st.error(f"數據解析錯誤: {e}")
        return None

# --- UI 渲染區 ---
input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if input_ticker:
    # 進行資料取得
    metrics = get_stock_metrics(input_ticker)
    ticker = yf.Ticker(input_ticker)
    
    # 檢查是否獲取到 ticker 資訊 (避免無效 ticker 導致崩潰)
    try:
        info = ticker.info
        if "currentPrice" not in info:
            st.warning("無法取得該代號的即時市場資訊。")
            st.stop()
    except Exception:
        st.error("連線 Yahoo Finance 失敗，請稍後再試。")
        st.stop()

    # 渲染區塊
    st.markdown(f"### 即時股價: {info.get('currentPrice', 'N/A')}")
    
    if metrics:
        st.subheader("📈 近期走勢互動圖表")
        hist = ticker.history(period="1mo")
        if not hist.empty:
            fig = px.line(hist, y="Close", title=f"{input_ticker} 近期走勢")
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🤖 AI 顧問分析")
        st.info(metrics.get('ai_insight', "AI 正在待命中..."))
    else:
        st.write("目前尚無此標的的進階籌碼分析數據。")
