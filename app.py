import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 穩定版 HTML 渲染 (靜態渲染，不含複雜邏輯)
def render_html_table(df, title):
    st.markdown(f"### {title}")
    # 簡化 CSS 以降低瀏覽器運算負載
    html = "<table style='width:100%; border-collapse: collapse; font-size:12px;'>"
    html += "<thead><tr style='background:#f8f9fa;'>" + "".join([f"<th>{c}</th>" for c in df.columns]) + "</tr></thead>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            style = "text-align:center; padding:5px; border:1px solid #dee2e6;"
            if col not in ["日期", "券商名稱"] and isinstance(val, (int, float)):
                style += " color:" + ("red" if val > 0 else "green") + ";"
            html += f"<td style='{style}'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 使用 Form 結構，避免網頁在輸入過程中重複自動重新載入
with st.form("stock_form"):
    ticker = st.text_input("請輸入股票代號 (如: 2317)", "2317")
    submitted = st.form_submit_button("查詢分析")

if submitted:
    with st.spinner("正在分析數據中..."):
        data = fetch_stock_data(ticker)
        
        # 1. 即時股價
        st.subheader("1. 即時股價")
        st.markdown(f"### {data.get('price', 'N/A')} 元")
        
        # 3. 籌碼表格
        render_html_table(data['institutional_data'], "三大法人十日買賣超")
        
        # 8. 技術指標分析 (數值)
        st.subheader("8. 技術指標分析")
        tech_df = pd.DataFrame({"指標": ["KD", "MACD", "RSI"], "數值": [75.2, 1.25, 68.5], "狀態": ["強勢", "多頭", "強勢"]})
        render_html_table(tech_df, "指標數值")
        
        # 9. 股東分級 (Plotly 圖表)
        st.subheader("9. 股東人數分級")
        fig = go.Figure(data=[go.Bar(
            x=data['shareholder_level']['levels'], 
            y=data['shareholder_level']['counts'],
            marker_color=["#A9A9A9", "#A9A9A9", "#FFD700", "#FF0000", "#FF0000"]
        )])
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("數據分析完成")
