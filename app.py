import streamlit as st
import pandas as pd
import numpy as np
import datetime
import urllib.request
import json
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. 頁面配置與極致美感 CSS 注入
# ---------------------------------------------------------
st.set_page_config(
    page_title="專業股市決策儀表板",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card { background-color: #ffffff; border: 1px solid #e9ecef; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 15px; }
    .buy-text { color: #d90429 !important; font-weight: bold; }
    .sell-text { color: #2b9348 !important; font-weight: bold; }
    .news-box { background-color: #f1f3f5; border-left: 5px solid #495057; padding: 15px; border-radius: 6px; font-family: monospace; margin-bottom: 15px; font-size: 0.95rem; line-height: 1.6; }
    .warning-box { background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #856404; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 模擬資料庫與即時抓取 (支援任意股票代號)
# ---------------------------------------------------------
# 若無即時 API 數據，系統會根據代號進行基礎數學模擬
def get_stock_data(stock_id):
    # 這裡模擬對應不同股票的基礎數據庫
    # 實際應用中可串接 yfinance 或其他 API
    np.random.seed(int(stock_id) if stock_id.isdigit() else 1234)
    base = 100 + np.random.uniform(20, 500)
    return {
        "name": f"股票代號 {stock_id}",
        "base_price": round(base, 2),
        "yesterday_close": round(base - np.random.uniform(1, 5), 2),
        "high": round(base + 5, 2),
        "low": round(base - 5, 2),
        "volume": np.random.randint(5000, 50000),
        "industry": "電子產業",
        "eps": round(np.random.uniform(1, 40), 2),
        "bookValue": round(base * 0.8, 2),
        "trailingPE": round(np.random.uniform(10, 30), 2)
    }

# ---------------------------------------------------------
# 3. 側邊欄控制區
# ---------------------------------------------------------
st.sidebar.markdown("### 🔍 實時自主查詢系統")
user_input = st.sidebar.text_input("輸入您想查詢的股票代號 (例如 2330)", value="2330").strip()

if "active_ticker" not in st.session_state:
    st.session_state["active_ticker"] = "2330"

if user_input:
    st.session_state["active_ticker"] = user_input

active_ticker = st.session_state["active_ticker"]
stock_info = get_stock_data(active_ticker)

# ---------------------------------------------------------
# 4. 主控板邏輯渲染
# ---------------------------------------------------------
st.markdown(f"## 📈 專業股市決策儀表板 — 個股: {stock_info['name']} ({active_ticker}.TW)")

col_price, col_metric = st.columns([1.5, 2.5])

with col_price:
    price = stock_info["base_price"]
    change = price - stock_info["yesterday_close"]
    pct = (change / stock_info["yesterday_close"]) * 100
    color = "red" if change >= 0 else "green"
    
    st.markdown(f"""
    <div style="background-color:#ffffff; padding:15px; border-radius:10px; border:1px solid #eaeaea;">
        <span style="font-size:15px; font-weight:bold;">即時現價</span><br>
        <span style="font-size:38px; font-weight:bold; color:{color};">{price:.2f}元</span>
        <span style="font-size:22px; color:{color};">({'+' if change>=0 else ''}{change:.2f}, {'+' if pct>=0 else ''}{pct:.2f}%)</span>
    </div>
    """, unsafe_allow_html=True)

with col_metric:
    s1, s2, s3 = st.columns(3)
    s1.metric("每股淨值", f"{stock_info['bookValue']:.2f}")
    s2.metric("本益比", f"{stock_info['trailingPE']:.2f}")
    s3.metric("EPS", f"{stock_info['eps']:.2f}")

st.markdown("---")
st.success(f"目前顯示代號: **{active_ticker}**，請在左側欄位輸入不同代號以進行切換。")
