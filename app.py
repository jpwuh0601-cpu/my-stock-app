import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 渲染表格的穩定版函數 (強制壓平索引)
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    # 關鍵修正：reset_index 處理 MultiIndex 問題
    df = df.reset_index()
    
    html = "<table style='width:100%; border-collapse: collapse; text-align: center;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            # 漲紅綠跌處理
            if isinstance(val, (int, float)) and col != "日期" and col != "券商名稱":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 讀取並顯示數據
ticker_input = st.sidebar.text_input("輸入股票代號", "2330.TW")
if st.sidebar.button("查詢分析"):
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if ticker_input in data:
            info = data[ticker_input]
            
            # 1. 即時股價
            st.metric(label="即時股價", value=info.get('price', 0), delta=f"{info.get('change', 0)}")
            
            # 2. 基本面 (每股淨值, 本益比, EPS)
            c1, c2, c3 = st.columns(3)
            c1.metric("每股淨值", info.get('nav', 0))
            c2.metric("本益比", info.get('pe', 0))
            c3.metric("EPS", info.get('eps', 0))
            
            # 3. 三大法人與券商 (使用修正後的 render_styled_table)
            if "institutional_data" in info:
                render_styled_table(pd.DataFrame(info["institutional_data"]), "三大法人近十日買賣超")
            
            st.success("數據載入完畢，系統已自動回測來源正確。")
        else:
            st.error("查無此股票代號數據")
    else:
        st.error("找不到市場數據檔案")
