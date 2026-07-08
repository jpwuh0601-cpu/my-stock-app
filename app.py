import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

def render_html_table(data_list, title):
    """安全渲染 HTML 表格"""
    st.markdown(f"### {title}")
    if not data_list or not isinstance(data_list, list) or len(data_list) == 0:
        st.info(f"目前無 {title} 資料")
        return
    
    df = pd.DataFrame(data_list)
    html = "<table style='width:100%; border-collapse: collapse; font-size:13px; text-align:center;'>"
    html += "<thead><tr style='background:#f0f0f0;'>" + "".join([f"<th style='padding:8px; border:1px solid #ccc;'>{c}</th>" for c in df.columns]) + "</tr></thead>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            style = "padding:6px; border:1px solid #ddd;"
            # 漲紅跌綠：針對數值欄位進行處理
            if col not in ["日期", "券商名稱"] and isinstance(val, (int, float)):
                style += " color:" + ("red" if val > 0 else "green") + "; font-weight:bold;"
            html += f"<td style='{style}'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

with st.form("stock_form"):
    ticker = st.text_input("輸入股票代號 (如: 2317)", "2317")
    submitted = st.form_submit_button("查詢分析")

if submitted:
    with st.spinner("正在讀取資料..."):
        data = fetch_stock_data(ticker) or {}
        
        # 1. 即時股價
        price = data.get('price', 'N/A')
        change = data.get('change', 0)
        st.subheader("1. 即時股價")
        st.markdown(f"### <span style='color: {'red' if change >= 0 else 'green'}'>{price} 元 ({'+' if change >= 0 else ''}{change} 元)</span>", unsafe_allow_html=True)
        
        # 2. 基本面
        st.subheader("2. 基本面資訊")
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨額", data.get('nav', 0))
        col2.metric("本益比", data.get('pe', 0))
        col3.metric("EPS", data.get('eps', 0))
        
        # 3. 籌碼細項
        render_html_table(data.get('institutional_data'), "三大法人十日買賣超細項")
        render_html_table(data.get('broker_data'), "十大主力券商十日買賣超細項")
        
        # 9. 股東分級 (修正 StreamlitColorLengthError)
        st.subheader("9. 股東人數與持股分級")
        levels = ['1-10張', '10-100張', '100-400張', '400-1000張', '1000張以上']
        counts = [100, 200, 150, 80, 20] # 示例數據
        # 顏色：灰色(散戶)、黃色(中戶/大戶區)、紅色(大戶)
        bar_colors = ['#A9A9A9', '#A9A9A9', '#FFD700', '#FF0000', '#FF0000']
        
        fig = go.Figure(data=[go.Bar(x=levels, y=counts, marker_color=bar_colors)])
        fig.update_layout(title="400張以上為大戶(紅色)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
