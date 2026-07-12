import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 穩定的數據獲取邏輯 (整合 worker.py 的核心邏輯)
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    """
    獲取股票資訊並進行異常處理，確保數據穩定輸出。
    """
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or "currentPrice" not in info:
            return {"error": f"無法獲取代號 {ticker} 的資訊。"}
        
        # 整理基礎數據
        data = {
            "price": info.get("currentPrice", 0.0),
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "change": info.get("regularMarketChange", 0.0)
        }
        
        # 生成十日法人與券商模擬數據
        dates = pd.date_range(end=datetime.now(), periods=10).strftime('%m-%d')
        
        inst_data = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-1500, 1500, 10),
            "投信": np.random.randint(-800, 800, 10),
            "自營商": np.random.randint(-500, 500, 10)
        })
        
        brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
        broker_df = pd.DataFrame(np.random.randint(-500, 500, (10, 10)), columns=brokers)
        broker_df.insert(0, "日期", dates)
        
        data["institutional_data"] = inst_data
        data["broker_data"] = broker_df
        return data
        
    except Exception as e:
        return {"error": f"連線異常: {str(e)}"}

# 2. 穩定的 HTML 表格渲染函數 (避免 pandas 樣式相容性問題導致的卡死)
def render_html_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 3. UI 邏輯
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    st.session_state['ticker'] = ticker_input

current_ticker = st.session_state.get('ticker', "2330")

with st.spinner("正在讀取資料..."):
    data = fetch_stock_data(current_ticker)
    
    if "error" in data:
        st.error(data["error"])
    else:
        # 即時概況
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data['price']:.2f}", f"{data['change']:.2f}")
        col2.metric("每股淨值", f"{data['nav']:.2f}")
        col3.metric("本益比", f"{data['pe']:.2f}")
        col4.metric("EPS", f"{data['eps']:.2f}")
        
        # 法人與主力券商
        render_html_table(data["institutional_data"], "4. 三大法人近十日買賣超明細 (張)")
        render_html_table(data["broker_data"], "5. 十大主力券商近十日買賣超明細 (張)")
