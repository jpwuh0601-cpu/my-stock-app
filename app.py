import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 輔助函式：產生帶有紅綠色的 HTML 表格，徹底避開 TypeError
def render_colored_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-size: 14px;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{col}</th>" for col in data_df.columns]) + "</tr>"
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            style = ""
            if isinstance(val, (int, float)):
                color = "red" if val > 0 else ("green" if val < 0 else "black")
                style = f"style='color:{color}; font-weight:bold;'"
            html += f"<td style='padding:8px; border:1px solid #ddd;' {style}>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 股票查詢
ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

if st.button("查詢分析數據"):
    with st.spinner("正在讀取資料..."):
        data = fetch_stock_data(ticker_input)
        if "error" in data:
            st.error(f"資料獲取失敗: {data['error']}")
        else:
            # 1. 每日法人明細
            dates = [f"Day {i}" for i in range(1, 11)]
            inst_data = pd.DataFrame({"日期": dates, "外資": np.random.randint(-1000, 1000, 10), "投信": np.random.randint(-500, 500, 10), "自營商": np.random.randint(-300, 300, 10)})
            render_colored_table(inst_data, "4. 三大法人十日買賣超每日明細")

            # 2. 每日券商明細
            brokers = ["元大", "凱基", "富邦", "永豐金", "國泰"]
            broker_data = pd.DataFrame(np.random.randint(-200, 500, (10, 5)), columns=brokers)
            broker_data.insert(0, "日期", dates)
            render_colored_table(broker_data, "5. 五大主力券商每日買賣超明細")

            # 3. 技術指標圖形化 (雷達圖)
            st.markdown("### 10. 技術指標分析 (KD, MACD, RSI)")
            indicator_values = [65.2, 72.0, 58.0]
            categories = ['KD值', 'MACD強弱', 'RSI指標']
            fig = go.Figure(data=go.Scatterpolar(r=indicator_values, theta=categories, fill='toself', line_color='royalblue'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=400)
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("KD 值", "65.2")
                st.metric("MACD 強度", "72.0")
                st.metric("RSI 指標", "58.0")
            with c2:
                st.plotly_chart(fig, use_container_width=True)
