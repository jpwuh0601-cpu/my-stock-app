import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go
from datetime import datetime

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

def load_market_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 載入數據
data = load_market_data()

if not data:
    st.warning("尚未載入數據，請先執行自動化分析任務。")
else:
    # 頂部指標卡片
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("即時股價", f"${data.get('price', 0):,.2f}")
    col2.metric("本益比 (PE)", data.get('pe_ratio', 'N/A'))
    col3.metric("每股盈餘 (EPS)", data.get('trailing_eps', 'N/A'))
    col4.metric("利潤率 (Margin)", f"{data.get('profit_margins', 0) * 100:.2f}%")

    # 主內容區
    tab1, tab2, tab3 = st.tabs(["📈 趨勢分析", "📋 詳細財報", "🤖 AI 洞察"])

    with tab1:
        st.subheader("股價與技術指標分析")
        # 這裡可以加入更多歷史數據繪圖邏輯
        fig = go.Figure(data=[go.Scatter(y=[data.get('price', 0)], mode='lines+markers', name="當前股價")])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("詳細財報數據")
        df = pd.DataFrame([data])
        st.table(df[['market_cap', 'book_value', 'total_revenue', 'debt_to_equity']])

    with tab3:
        st.subheader("AI 智能分析洞察")
        st.info(data.get('ai_prediction', "暫無 AI 分析結果"))
        
        st.subheader("籌碼面資訊")
        investors = data.get('institutional_investors', [])
        if investors:
            st.write(f"機構動向: {investors[0].get('機構')}, 買賣超: {investors[0].get('買賣超')}")

# 頁尾更新時間
st.sidebar.markdown(f"---")
st.sidebar.write(f"最後更新時間: {data.get('update_date', '未知')}")
