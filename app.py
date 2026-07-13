import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 穩定版資料獲取 (使用快取避免頻繁 API 呼叫)
@st.cache_data(ttl=300)
def get_data_cached(ticker):
    # worker.py 中的 fetch_stock_data 函數
    return fetch_stock_data(ticker)

# 穩定的 HTML 表格渲染函數 (避免 pandas 樣式相容性問題)
def render_html_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            # 針對數字進行漲紅跌綠處理
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data = get_data_cached(ticker)
        
        if "error" in data:
            st.error(f"⚠️ {data['error']}")
        else:
            # 1. 股價顯示 (股價顯示修正版)
            price = data.get('price', 0)
            change = data.get('change', 0)
            color_code = "red" if change >= 0 else "green"
            symbol = "▲" if change >= 0 else "▼"
            
            st.markdown(f"### 即時股價: {price}")
            st.markdown(f"**漲跌: <span style='color:{color_code}; font-size:20px;'>{symbol} {abs(change)} 元</span>**", unsafe_allow_html=True)
            
            # 2. 基本面數據
            col1, col2, col3 = st.columns(3)
            col1.metric("每股淨值", f"{data.get('nav', 0):.2f}")
            col2.metric("本益比", f"{data.get('pe', 0):.2f}")
            col3.metric("EPS", f"{data.get('eps', 0):.2f}")

            # 3. 法人數據
            if 'institutional_data' in data and not data['institutional_data'].empty:
                render_html_table(data['institutional_data'], "三大法人近十日買賣超明細 (張)")

            # 4. 主力券商數據 (主力券商修正版)
            if 'broker_data' in data and not data['broker_data'].empty:
                render_html_table(data['broker_data'], "十大主力券商近十日買賣超明細 (張)")

            # 5. 技術指標圖形化
            st.markdown("### 技術指標趨勢")
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
            st.plotly_chart(fig, use_container_width=True)
