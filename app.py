import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 穩定的 HTML 表格渲染
def render_stable_table(df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            style = "padding:8px; border:1px solid #ddd;"
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                style += f" color:{color}; font-weight:bold;"
            html += f"<td style='{style}'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 2. 籌碼大戶分析圖表
def plot_smart_money(data_df):
    st.markdown("### 📊 大戶與散戶籌碼動向")
    fig = go.Figure()
    
    # 判斷大戶( >400) 與 散戶 (<=400)
    for col in ["外資", "投信", "自營商"]:
        # 標記大戶
        big_money = np.where(data_df[col] > 400, data_df[col], 0)
        small_money = np.where(data_df[col] <= 400, data_df[col], 0)
        
        fig.add_trace(go.Bar(x=data_df["日期"], y=big_money, name=f"{col} (大戶)", marker_color='red'))
        fig.add_trace(go.Bar(x=data_df["日期"], y=small_money, name=f"{col} (散戶)", marker_color='green'))

    fig.update_layout(barmode='group', height=400, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# 主 UI
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在執行籌碼視覺化分析..."):
        # 模擬數據
        dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
        inst_data = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-600, 800, 10),
            "投信": np.random.randint(-200, 500, 10),
            "自營商": np.random.randint(-300, 300, 10)
        })

        # 1. 籌碼柱狀圖
        plot_smart_money(inst_data)

        # 2. 買賣超表格
        render_stable_table(inst_data, "三大法人近十日買賣超明細 (張)")

        # 3. 黑天鵝與風險監控
        st.markdown("### 4. 黑天鵝風險監控")
        st.warning("【地緣政治】俄烏戰爭與中東局勢動盪，建議關注能源相關個股風險溢價。")
        st.warning("【聯準會】利率政策維持高檔，市場資金流動性偏緊。")
