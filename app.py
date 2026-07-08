import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 穩定版資料讀取
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

# 渲染數據表格 (避免 MultiIndex 錯誤)
def render_clean_table(df, title):
    st.markdown(f"### {title}")
    # 強制壓平索引
    df = df.reset_index(drop=True)
    # 使用 streamlit dataframe，這比 st.table 更穩定
    st.dataframe(df, use_container_width=True)

# 標題與輸入
st.title("📈 專業股市決策儀表板")
data = load_data()
ticker = st.sidebar.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")

if st.sidebar.button("查詢分析數據"):
    if not data:
        st.error("系統讀不到 market_data.json，請確認 main_task.py 是否已執行。")
    elif ticker not in data:
        st.error(f"找不到 {ticker} 的數據。目前庫存代號: {list(data.keys())}")
    else:
        info = data[ticker]
        
        # 1. & 2. 基本財務數據
        st.subheader("1. 即時資訊與基本財務")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", info.get('price', 0), f"{info.get('change', 0)}")
        col2.metric("每股淨值", info.get('nav', 0))
        col3.metric("本益比", info.get('pe', 0))
        col4.metric("每股盈餘(EPS)", info.get('eps', 0))
        
        # 3. 三大法人
        if "institutional_data" in info:
            render_clean_table(pd.DataFrame(info["institutional_data"]), "3. 三大法人近十日買賣超")
        
        # 4 & 5. 財報與券商
        col_r1, col_r2 = st.columns(2)
        col_r1.info(f"**4. 財務季報摘要**\n\n{info.get('quarterly_reports', '無資料')}")
        col_r2.warning(f"**5. 主力券商分析**\n\n{info.get('broker_data', '無資料')}")
        
        # 6 & 7. AI預測與營收
        col_r3, col_r4 = st.columns(2)
        col_r3.success(f"**6. AI 財報預測**\n\n{info.get('ai_prediction', '無資料')}")
        col_r4.info(f"**7. 營收成長預估**\n\n{info.get('revenue_forecast', '無資料')}")
        
        # 8 & 9. 新聞與黑天鵝
        st.subheader("8 & 9. 市場監控與風險警示")
        st.text(f"【新聞】: {info.get('news', '無最新新聞')}")
        st.error(f"【黑天鵝警示】: {info.get('black_swan', '安全')}")
        
        # 10. 技術指標與股權分級
        st.subheader("10. 技術指標與持股結構")
        col_t1, col_t2 = st.columns(2)
        
        # 技術指標儀表
        tech = info.get('tech_indicators', {})
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = tech.get('KD', 50),
            title = {'text': "KD 指標"},
            gauge = {'axis': {'range': [0, 100]}}
        ))
        col_t1.plotly_chart(fig, use_container_width=True)
        
        # 股權分級柱狀圖
        struct = info.get('shareholder_structure', {})
        col_t2.bar_chart(pd.DataFrame(struct, index=[0]).T)
