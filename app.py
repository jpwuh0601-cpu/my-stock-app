import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from worker import fetch_stock_data

# 1. 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 2. 資料獲取與快取 (防止重複呼叫 API)
@st.cache_data(ttl=300)
def get_data_cached(ticker):
    return fetch_stock_data(ticker)

# 3. HTML 表格渲染函數 (穩定呈現數據，避免樣式衝突)
def render_html_table(data_df, title):
    st.markdown(f"### {title}")
    if data_df.empty:
        st.info("暫無詳細數據")
        return
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            # 數值漲紅跌綠判斷
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 4. 側邊欄互動
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data = get_data_cached(ticker)
        
        if "error" in data:
            st.error(f"⚠️ {data['error']}")
        else:
            # 股價資訊顯示
            price = data.get('price', 0)
            change = data.get('change', 0)
            color_code = "red" if change >= 0 else "green"
            symbol = "▲" if change >= 0 else "▼"
            
            st.markdown(f"### 即時股價: {price}")
            st.markdown(f"**漲跌: <span style='color:{color_code}; font-size:20px;'>{symbol} {abs(change)} 元</span>**", unsafe_allow_html=True)
            
            # 基本面數據
            col1, col2, col3 = st.columns(3)
            col1.metric("每股淨值", f"{data.get('nav', 0):.2f}")
            col2.metric("本益比", f"{data.get('pe', 0):.2f}")
            col3.metric("EPS", f"{data.get('eps', 0):.2f}")

            # 數據表格呈現
            if 'institutional_data' in data:
                render_html_table(data['institutional_data'], "三大法人近十日買賣超明細 (張)")

            if 'broker_data' in data:
                render_html_table(data['broker_data'], "十大主力券商近十日買賣超明細 (張)")

            # 技術指標圖形化
            st.markdown("### 技術指標趨勢")
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
            st.plotly_chart(fig, use_container_width=True)
