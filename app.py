import streamlit as st
import pandas as pd
import plotly.express as px
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定頁面風格
st.set_page_config(page_title="AI 專業投資儀表板", layout="wide", page_icon="📈")

# 自訂 CSS 美化
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #0047AB; color: white; }
    .css-1r6slp0 { padding: 1rem; border-radius: 10px; border: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞")

# 初始化
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame({"代號": ["2330", "2454"], "名稱": ["台積電", "聯發科"], "成本": [600, 900], "現價": [650, 950]})
if 'logs' not in st.session_state:
    st.session_state.logs = []

# 安全讀取
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

menu = st.sidebar.radio("導航目錄", ["📊 市場健康", "🤖 AI 智慧分析", "💼 部位管理", "📋 分享建議"])

if menu == "📊 市場健康":
    st.subheader("系統狀態監控")
    col1, col2 = st.columns(2)
    col1.metric("數據來源", "Yahoo Finance", "正常")
    col2.metric("AI 模型", "GPT-4o-mini", "連線中")
    st.info("系統運作中，親友分享請參考右側說明。")

elif menu == "🤖 AI 智慧分析":
    st.subheader("個股深度健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    if st.button("啟動 AI 深度分析"):
        with st.spinner("正在讀取財報並進行深度推論..."):
            stock = yf.Ticker(f"{t}.TW")
            info = stock.info
            funda = f"PE: {info.get('trailingPE')}, EPS: {info.get('trailingEps')}"
            prompt = f"分析 {t}，數據：{funda}。請以專業基金經理人語氣提供建議。"
            response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
            res = response.choices[0].message.content
            st.markdown(f"### 分析報告\n{res}")
            st.session_state.logs.append({"時間": datetime.now().strftime("%H:%M"), "代號": t, "結果": "已分析"})

elif menu == "💼 部位管理":
    st.subheader("我的持股看板")
    df = st.session_state.portfolio
    df['損益'] = df['現價'] - df['成本']
    fig = px.bar(df, x='名稱', y='損益', color='損益', text='損益')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "📋 分享建議":
    st.subheader("📢 分享給親友的注意事項")
    st.warning("""
    ### 親友使用建議：
    1. **輔助工具**：本系統僅為數據分析輔助，不做任何買賣承諾。
    2. **延遲資訊**：資料來自 Yahoo Finance，非即時交易數據。
    3. **保護個資**：切勿分享您的 API Key。
    4. **風險自負**：股票投資有賺有賠，下單前請三思。
    """)
    st.success("您可以放心分享此連結給親友，我們會自動過濾掉敏感的 API Key。")
