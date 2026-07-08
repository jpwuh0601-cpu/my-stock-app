import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- 頁面配置 ---
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# --- 輔助函式：顏色樣式 ---
def get_color(value):
    return "red" if value > 0 else "green"

def render_styled_table(df, title):
    st.markdown(f"### {title}")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px;'>"
    html += "<tr>" + "".join([f"<th style='padding:8px; border:1px solid #ddd; background:#f4f4f4;'>{c}</th>" for c in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            if isinstance(val, (int, float)) and col != "日期" and col != "券商名稱":
                color = get_color(val)
                html += f"<td style='padding:8px; border:1px solid #ddd; color:{color}; font-weight:bold;'>{val}</td>"
            else:
                html += f"<td style='padding:8px; border:1px solid #ddd;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# --- 側邊欄輸入 ---
ticker = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取數據並執行 AI 分析..."):
        # 模擬數據獲取 (請接上您的 worker.py)
        # 這裡用模擬數據確保版面符合需求
        
        # 1 & 2. 股價與基本面 (Metrics)
        st.markdown(f"## {ticker} 即時分析報告")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("即時股價", "650.0", "+5.2 (紅)")
        c2.metric("每股淨值", "120.5")
        c3.metric("本益比", "22.1")
        c4.metric("EPS", "38.2")

        # 3. 財報區
        with st.expander("📊 今年與去年每季財報比較"):
            st.write("表格：[去年Q1-Q4 | 今年Q1-Q2]")
        
        # 4 & 5. 法人與主力券商表格 (彩色)
        col_left, col_right = st.columns(2)
        with col_left:
            inst_data = pd.DataFrame({'日期': ['07-08', '07-07'], '外資': [500, -200], '投信': [-100, 300]})
            render_styled_table(inst_data, "三大法人十日買賣超")
        with col_right:
            broker_data = pd.DataFrame({'券商名稱': ['元大', '凱基'], '買賣超': [800, -400]})
            render_styled_table(broker_data, "十家券商十日買賣超")

        # 6. AI 財報預測與自動化回測
        st.markdown("---")
        st.markdown("### 🤖 AI 財報預測與數據驗證")
        st.info("AI 預測: 營收成長率 15%, EPS 預估 42.5元。自動回測: 資料來源準確率 99.8% (OK)")
        
        # 7. 營收、EPS、股利預估
        st.markdown("### 🔮 營收與股利預估")
        st.write("今年預估營收: 2.5兆 | EPS: 42.5元 | 預估股利: 18.5元")

        # 8 & 9. 新聞與黑天鵝
        col_news, col_swan = st.columns(2)
        with col_news:
            st.markdown("### 📰 即時股市新聞")
            for i in range(3):
                st.write(f"{i+1}. 股市快訊: 市場看好半導體復甦，預期供應鏈將在下半年迎來強勁補單潮，激勵台股表現。")
        with col_swan:
            st.markdown("### 🦢 黑天鵝警示")
            st.warning("1. 俄烏戰爭: 局勢升級，能源成本恐受波及。")
            st.warning("2. 美伊戰爭: 中東地緣政治風險上升。")
            st.warning("3. 聯準會: 利率維持高檔，市場資金緊縮。")

        # 10. 技術指標圖形 (KD, MACD, RSI)
        st.markdown("### 📈 技術指標分析")
        fig_tech = go.Figure()
        fig_tech.add_trace(go.Scatter(y=[20, 50, 80], name="KD值"))
        fig_tech.add_trace(go.Scatter(y=[0, 10, -5], name="MACD"))
        st.plotly_chart(fig_tech, use_container_width=True)

        # 11. 股東人數分級
        st.markdown("### 👥 股東持股分級")
        sh_data = pd.DataFrame({
            '分級': ['1-10張', '100-400張', '1000張以上'],
            '人數': [10000, 500, 50],
            'color': ['gray', 'yellow', 'red']
        })
        fig_bar = px.bar(sh_data, x='分級', y='人數', color='color', color_discrete_map="identity")
        st.plotly_chart(fig_bar, use_container_width=True)

        # 12. 即時新聞 (時事第物)
        st.markdown("### ⏱️ 即時股市資訊 (時事第物)")
        st.table(pd.DataFrame({
            "時間": ["09:00", "10:00"],
            "事實": ["台積電開高", "盤中震盪"],
            "第(地)點": ["台北證交所", "電子科技園區"],
            "物(物件)": ["台積電股票", "外資買單"]
        }))
