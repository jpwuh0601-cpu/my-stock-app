import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 輔助函式：產生帶有紅綠色的 HTML 表格
def render_colored_table(data_df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-size: 14px;'>"
    # 表頭
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{col}</th>" for col in data_df.columns]) + "</tr>"
    # 內容
    for _, row in data_df.iterrows():
        html += "<tr>"
        for col in data_df.columns:
            val = row[col]
            # 判斷顏色：數值型且大於0紅色，小於0綠色
            style = ""
            if isinstance(val, (int, float)):
                color = "red" if val > 0 else ("green" if val < 0 else "black")
                style = f"style='color:{color}; font-weight:bold;'"
            html += f"<td style='padding:8px; border:1px solid #ddd;' {style}>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# --- 1. 三大法人每日明細 ---
st.markdown("### 4. 三大法人十日買賣超每日明細")
dates = [f"Day {i}" for i in range(1, 11)]
inst_data = pd.DataFrame({
    "日期": dates,
    "外資": np.random.randint(-1000, 1000, 10),
    "投信": np.random.randint(-500, 500, 10),
    "自營商": np.random.randint(-300, 300, 10)
})
render_colored_table(inst_data, "")

# --- 2. 十大主力券商每日明細 ---
st.markdown("### 5. 十大主力券商每日買賣超明細")
brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南永昌", "兆豐", "統一"]
# 模擬十天資料
broker_data = pd.DataFrame(np.random.randint(-200, 500, (10, 10)), columns=brokers)
broker_data.insert(0, "日期", dates)
render_colored_table(broker_data, "")

# --- 3. 技術指標圖形化 ---
st.markdown("### 10. 技術指標分析 (KD, MACD, RSI)")
# 模擬指標數值 (0-100 正規化)
indicator_values = [65.2, 72.0, 58.0] # KD, MACD, RSI
categories = ['KD值', 'MACD強弱', 'RSI指標']

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=indicator_values,
      theta=categories,
      fill='toself',
      line_color='royalblue'
))

fig.update_layout(
  polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
  showlegend=False,
  height=400
)

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("KD 值", "65.2")
    st.metric("MACD 強度", "72.0")
    st.metric("RSI 指標", "58.0")
with col2:
    st.plotly_chart(fig, use_container_width=True)
