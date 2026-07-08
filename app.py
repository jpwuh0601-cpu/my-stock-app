import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 渲染法人/券商表格
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    df = df.reset_index(drop=True)
    html = "<table style='width:100%; border-collapse: collapse; text-align: center;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期":
                color = "red" if val > 0 else "green"
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

data = load_data()
ticker = st.sidebar.text_input("輸入股票代號", "2330.TW")

if st.sidebar.button("查詢分析"):
    if ticker in data:
        info = data[ticker]
        
        # 1. 即時股價
        st.metric("即時股價", info['price'], f"{info['change']} 元")
        
        # 2. 基本面數據
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", info['nav'])
        c2.metric("本益比", info['pe'])
        c3.metric("EPS", info['eps'])
        
        # 3. 報表與籌碼
        st.subheader("3. 財務與籌碼報表")
        st.write(f"季報摘要: {info['quarterly_reports']}")
        render_styled_table(pd.DataFrame(info["institutional_data"]), "三大法人買賣超 (10日)")
        
        # 4 & 5. AI 與預估數據
        col_a, col_b = st.columns(2)
        col_a.success(f"AI財報預測: {info['ai_prediction']}")
        col_b.warning(f"營收與股利: {info['revenue_forecast']}")
        
        # 6, 7 & 10. 新聞與黑天鵝
        st.subheader("即時新聞與風險警示")
        st.markdown(f"**📰 即時新聞**: {info['news']}")
        st.error(f"⚠️ 黑天鵝警示: {info['black_swan']}")
        
        # 8. 技術指標圖形化
        st.subheader("8. 技術指標")
        tech_df = pd.DataFrame([info['tech_indicators']])
        st.bar_chart(tech_df)
        
        # 9. 股東結構 (柱狀體)
        st.subheader("9. 股東結構分析")
        sh_data = info['shareholder_structure']
        # 定義顏色對應
        colors = ['gray', 'yellow', 'red']
        df_sh = pd.DataFrame(list(sh_data.values()), index=list(sh_data.keys()), columns=['持股比例'])
        st.bar_chart(df_sh)
        
    else:
        st.error("查無此股票代號數據")
