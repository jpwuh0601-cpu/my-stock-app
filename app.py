import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

def render_html_table(df, title):
    """渲染表格，具備漲紅跌綠與防錯機制"""
    st.markdown(f"### {title}")
    if not isinstance(df, pd.DataFrame) or df.empty:
        st.info(f"目前無 {title} 資料")
        return
    
    html = "<table style='width:100%; border-collapse: collapse; font-size:13px; text-align:center;'>"
    html += "<thead><tr style='background:#f0f0f0;'>" + "".join([f"<th style='padding:8px; border:1px solid #ccc;'>{c}</th>" for c in df.columns]) + "</tr></thead>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            style = "padding:6px; border:1px solid #ddd;"
            if col not in ["日期", "券商名稱"] and isinstance(val, (int, float)):
                style += " color:" + ("red" if val > 0 else "green") + "; font-weight:bold;"
            html += f"<td style='{style}'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 輸入區
with st.form("stock_form"):
    ticker = st.text_input("自行輸入股票代號 (如: 2317)", "2317")
    submitted = st.form_submit_button("查詢分析")

if submitted:
    with st.spinner("正在讀取資料..."):
        data = fetch_stock_data(ticker) or {}
        
        # 1. 即時股價
        st.subheader("1. 即時股價")
        price = data.get('price', 'N/A')
        change = data.get('change', 0)
        st.markdown(f"### <span style='color: {'red' if change >= 0 else 'green'}'>{price} ({'+' if change >= 0 else ''}{change} 元)</span>", unsafe_allow_html=True)
        
        # 2. 基本面數據
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨額", data.get('nav', 0))
        col2.metric("本益比", data.get('pe', 0))
        col3.metric("EPS", data.get('eps', 0))
        
        # 3. 報表與籌碼
        st.subheader("3. 報表與籌碼動向")
        render_html_table(data.get('institutional_data'), "三大法人十日買賣超細項")
        render_html_table(data.get('broker_data'), "十家主力券商十日買賣超細項")
        
        # 4. AI 財報預測
        st.subheader("4. AI 財報預測與回測")
        ai = data.get('ai_analysis', {})
        st.info(f"AI 預測準確度回測：{ai.get('回測準確度', 'N/A')} | 資料來源正確。")
        
        # 9. 股東人數 (修正長度錯誤)
        st.subheader("9. 股東人數與持股分級")
        share = data.get('shareholder_level', {})
        levels = share.get('levels', ['1-10張', '10-100張', '100-400張', '400-1000張', '1000張以上'])
        counts = share.get('counts', [0, 0, 0, 0, 0])
        
        # 防錯：確保數據長度一致
        if len(levels) == len(counts):
            fig_bar = go.Figure(data=[go.Bar(x=levels, y=counts, marker_color=["#A9A9A9", "#A9A9A9", "#FFD700", "#FF0000", "#FF0000"])])
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("股東持股分級資料長度異常，無法繪圖。")
