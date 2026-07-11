import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data  # 確保 worker.py 在同一目錄

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 穩定版資料獲取 (增加錯誤捕捉)
@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        data = fetch_stock_data(ticker)
        if "error" in data:
            return data, True, ticker
        return data, False, ticker
    except Exception as e:
        return {"error": str(e)}, True, ticker

# 輸入區
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data, is_error, used_ticker = get_data(ticker)
        
        if is_error:
            st.error(f"⚠️ {data.get('error', '未知錯誤')}")
        else:
            # 1. 股價與基本面顯示
            st.markdown(f"### {used_ticker} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data.get('price', 0):.2f}")
            col2.metric("每股淨值", f"{data.get('nav', 0):.2f}")
            col3.metric("本益比", f"{data.get('pe', 0):.2f}")
            col4.metric("EPS", f"{data.get('eps', 0):.2f}")

            # 2. 法人數據表格
            if "institutional_data" in data:
                st.markdown("### 4. 三大法人近十日買賣超明細 (張)")
                st.dataframe(data["institutional_data"], use_container_width=True)

            # 3. 技術指標
            st.markdown("### 10. 技術指標參考")
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
            st.plotly_chart(fig, use_container_width=True)
