import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. HTML 樣式渲染函式 (解決 StreamlitAPIException)
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    # 將所有數值轉為帶顏色的 HTML 標籤
    html = "<table style='width:100%; border-collapse: collapse; text-align: center;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期" and col != "券商名稱":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 載入數據
def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

ticker_input = st.sidebar.text_input("輸入股票代號", "2330.TW")

if st.sidebar.button("查詢分析"):
    data = load_data()
    if ticker_input in data:
        info = data[ticker_input]
        
        # 1. 股價與漲跌 (紅漲綠跌)
        price = info.get('price', 0)
        change = info.get('change', 0)
        st.metric(label="即時股價", value=price, delta=f"{change}")
        
        # 2. 基本面 (每股淨值, 本益比, EPS)
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", info.get('nav', 0))
        c2.metric("本益比", info.get('pe', 0))
        c3.metric("EPS", info.get('eps', 0))
        
        # 3. 法人與券商 (表格渲染)
        render_styled_table(pd.DataFrame(info.get("institutional_data", [])), "三大法人近十日買賣超")
        
        # 4-10. 其他區塊... (請依照此邏輯擴充)
        st.markdown("### AI 財報預測與回測")
        st.success(info.get("ai_prediction", "模型預測中..."))
        
        st.markdown("### 技術指標 (KD/MACD/RSI)")
        # 這裡放置您的 Plotly 圖表
        
    else:
        st.error("查無此股票數據")
