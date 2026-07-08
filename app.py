import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 穩定的 HTML 表格渲染 (漲紅跌綠)
def render_stable_table(df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-size: 14px; text-align: center;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#eee;'>{c}</th>" for c in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            style = "padding:8px; border:1px solid #ddd;"
            if isinstance(val, (int, float)) and col not in ["日期", "券商名稱"]:
                color = "red" if val > 0 else "green"
                style += f" color:{color}; font-weight:bold;"
            html += f"<td style='{style}'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 2. 股東分級圖表 (指定顏色)
def plot_shareholder_structure():
    st.markdown("### 📊 股東人數與持股分級")
    levels = ["1-10張", "10-100張", "100-400張", "400-1000張", "1000張以上"]
    counts = [5000, 2000, 800, 300, 150]
    # 1-10張灰色, 100-400張黃色, 1000張以上紅色
    colors = ["#A9A9A9", "#D3D3D3", "#FFD700", "#FFA500", "#FF0000"]
    fig = go.Figure(data=[go.Bar(x=levels, y=counts, marker_color=colors)])
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# 主邏輯
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")
if st.button("查詢分析"):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
    
    # 籌碼數據生成
    inst_data = pd.DataFrame({
        "日期": dates, 
        "外資": np.random.randint(-1000, 1000, 10), 
        "投信": np.random.randint(-500, 500, 10), 
        "自營商": np.random.randint(-300, 300, 10)
    })
    
    # 十大券商數據生成
    brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
    broker_df = pd.DataFrame(np.random.randint(-500, 500, (10, 10)), columns=brokers)
    broker_df.insert(0, "日期", dates)

    # 顯示版面
    render_stable_table(inst_data, "三大法人十日買賣超細項")
    render_stable_table(broker_df, "主力券商十日買賣超細項")
    plot_shareholder_structure()
    st.write("註：柱狀圖紅、黃、灰色顯示持股等級；法人與券商買賣超紅綠顯示漲跌動能。")
