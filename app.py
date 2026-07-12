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
# 2. 數據庫與模擬機制 (支援動態輸入)
# ---------------------------------------------------------
def get_stock_data(stock_id):
    # 使用固定 Seed 以確保滑桿調整時數據不隨機跳動
    np.random.seed(int(stock_id) if stock_id.isdigit() else 1234)
    # 模擬基礎數據
    base = np.random.uniform(20, 1000)
    change_val = np.random.uniform(-5, 5)
    return {
        "name": f"個股 ({stock_id})",
        "price": round(base, 2),
        "yesterday_close": round(base - change_val, 2),
        "high": round(base + 2.5, 2),
        "low": round(base - 2.5, 2),
        "volume": np.random.randint(1000, 50000),
        "industry": "電子產業",
        "eps": round(np.random.uniform(0.5, 30), 2),
        "bookValue": round(base * 0.7, 2),
        "trailingPE": round(np.random.uniform(10, 50), 2)
    }

# ---------------------------------------------------------
# 3. 側邊欄控制區
# ---------------------------------------------------------
st.sidebar.markdown("### 🔍 實時自主查詢系統")
user_input = st.sidebar.text_input("輸入您想查詢的股票代號", value="2330").strip()

if "active_ticker" not in st.session_state:
    st.session_state["active_ticker"] = "2330"

if user_input:
    st.session_state["active_ticker"] = user_input

active_ticker = st.session_state["active_ticker"]
stock_info = get_stock_data(active_ticker)

# ---------------------------------------------------------
# 4. 主控板邏輯渲染
# ---------------------------------------------------------
st.markdown(f"## 📈 專業股市決策儀表板 — {stock_info['name']}")

price = stock_info["price"]
change = price - stock_info["yesterday_close"]
pct = (change / stock_info["yesterday_close"]) * 100
color = "red" if change >= 0 else "green"
symbol = "▲" if change >= 0 else "▼"

# 漲跌顯示區
st.markdown(f"""
<div class="metric-card">
    <span style="font-size:18px; font-weight:bold;">即時現價</span><br>
    <span style="font-size:48px; font-weight:bold; color:{color};">{price:.2f} 元</span>
    <span style="font-size:24px; color:{color}; font-weight:bold; margin-left:20px;">
        {symbol} {abs(change):.2f} ({pct:+.2f}%)
    </span>
</div>
""", unsafe_allow_html=True)

# 指標區
col1, col2, col3 = st.columns(3)
col1.metric("每股淨值 (元)", f"{stock_info['bookValue']:.2f}")
col2.metric("本益比 (倍)", f"{stock_info['trailingPE']:.2f}")
col3.metric("每股盈餘 (元)", f"{stock_info['eps']:.2f}")

st.markdown("---")
st.info(f"當前監控代號：{active_ticker}。系統已更新數據。")
