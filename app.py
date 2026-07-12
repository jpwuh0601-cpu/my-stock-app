import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. 頁面配置 ---
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

st.markdown("""
<style>
    .reportview-container { background-color: #FAFAFA; }
    .metric-card {
        padding: 18px; border: 1px solid #E2E8F0; border-radius: 8px; 
        background: #FFF; height: 125px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 純本地模擬數據引擎 (保證秒開不卡頓) ---
def get_mock_data(ticker_input):
    ticker = ticker_input.strip().upper()
    ticker_code = "".join(filter(str.isdigit, ticker))
    if not ticker_code: ticker_code = "2330"
    
    # 建立一個簡單的本地資料庫
    db = {
        "2330": {"name": "台積電", "price": 945.0, "change": 12.0, "nav": 142.5, "pe": 28.5, "eps": 33.15},
        "2317": {"name": "鴻海", "price": 185.5, "change": -1.5, "nav": 105.2, "pe": 18.2, "eps": 10.19},
        "2454": {"name": "聯發科", "price": 1210.0, "change": 15.0, "nav": 218.0, "pe": 24.1, "eps": 50.21},
    }
    
    base_data = db.get(ticker_code, {
        "name": f"自選股-{ticker_code}", "price": 100.0, "change": 0.0, 
        "nav": 50.0, "pe": 15.0, "eps": 5.0
    })
    base_data["ticker"] = f"{ticker_code}.TW"
    
    # 模擬法人與券商數據
    dates = [(datetime.today() - timedelta(days=i)).strftime('%m-%d') for i in range(10)]
    dates.reverse()
    
    base_data["inst_data"] = pd.DataFrame({
        "日期": dates,
        "外資": np.random.randint(-1500, 1500, 10),
        "投信": np.random.randint(-500, 500, 10),
        "自營商": np.random.randint(-300, 300, 10)
    })
    
    brokers = ["元大", "凱基", "富邦", "永豐金", "國泰"]
    base_data["broker_data"] = pd.DataFrame(
        np.random.randint(-800, 800, (10, 5)), columns=brokers
    )
    base_data["broker_data"].insert(0, "日期", dates)
    
    return base_data

# --- 3. 穩定版 HTML 表格渲染 ---
def render_html_table(df, title):
    st.markdown(f"### 📊 {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif; text-align: center;'>"
    html += "<tr style='background-color:#F8F9FA; border-bottom:2px solid #E2E8F0;'>"
    for col in df.columns:
        html += f"<th style='padding:10px; color:#4A5568;'>{col}</th>"
    html += "</tr>"
    for _, row in df.iterrows():
        html += "<tr style='border-bottom:1px solid #EDF2F7;'>"
        for col in df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期":
                color = "#E53E3E" if val > 0 else ("#319795" if val < 0 else "#4A5568")
                sign = "+" if val > 0 else ""
                html += f"<td style='padding:8px; color:{color}; font-weight:bold;'>{sign}{val:,}</td>"
            else:
                html += f"<td style='padding:8px; color:#2D3748;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# --- 側邊欄與主要畫面 ---
st.sidebar.markdown("## 🔍 股票查詢系統 (安全模式)")
ticker_input = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("獲取資料"):
    with st.spinner("正在讀取本地數據庫..."):
        data = get_mock_data(ticker_input)
        
        st.title(f"📈 專業股市決策儀表板 — {data['name']} ({data['ticker']})")
        
        # 1. 頂部四大指標
        col1, col2, col3, col4 = st.columns(4)
        is_up = data['change'] >= 0
        color = "#E53E3E" if is_up else "#319795"
        sym = "▲" if is_up else "▼"
        pct = (data['change'] / (data['price'] - data['change'])) * 100 if data['price'] else 0
        
        col1.markdown(f"<div class='metric-card'>即時股價<br><h2 style='color:{color}; margin:0;'>{data['price']:.2f} <span style='font-size:14px'>({sym} {abs(data['change']):.2f}, {pct:+.2f}%)</span></h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'>每股淨值 (NAV)<br><h2 style='color:#2D3748; margin:0;'>{data['nav']:.2f}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card'>歷史本益比 (PE)<br><h2 style='color:#2D3748; margin:0;'>{data['pe']:.2f}</h2></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='metric-card'>每股盈餘 (EPS)<br><h2 style='color:#2D3748; margin:0;'>{data['eps']:.2f}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. 表格區塊
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            render_html_table(data["inst_data"], "三大法人十日買賣超 (張)")
        with t_col2:
            render_html_table(data["broker_data"], "主力券商十日買賣超 (張)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3. 簡單技術指標圖表 (確保可視化元件不會卡死)
        st.markdown("### 🎯 技術指標狀態")
        fig = go.Figure(data=go.Scatterpolar(
            r=[75, 60, 85],
            theta=['KD指標', 'MACD動能', 'RSI強弱'],
            fill='toself',
            marker=dict(color='#E53E3E')
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("請於左側欄輸入股票代號並點擊「獲取資料」以開始使用。")
