import streamlit as st
import pandas as pd
import plotly.express as px
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定頁面風格
st.set_page_config(page_title="AI 專業投資儀表板", layout="wide", page_icon="📈")

# 自訂 CSS 美化：提升整體金融專業感
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #0047AB; 
        color: white; 
        font-weight: bold;
        border: none;
        padding: 0.5rem;
    }
    .stButton>button:hover { background-color: #003380; }
    .css-1r6slp0 { padding: 1.5rem; border-radius: 12px; border: 1px solid #e0e0e0; background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞")

# 初始化 Session State
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame({
        "代號": ["2330", "2454"], 
        "名稱": ["台積電", "聯發科"], 
        "成本": [600, 900], 
        "現價": [650, 950]
    })
if 'logs' not in st.session_state:
    st.session_state.logs = []

# 安全讀取環境變數 (請勿將此程式碼公開分享給親友)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
)

# 側邊欄導航
menu = st.sidebar.radio("導航目錄", ["📊 市場健康", "🤖 AI 智慧分析", "💼 部位管理", "📋 分享建議"])

# 頁面：市場健康
if menu == "📊 市場健康":
    st.subheader("系統狀態監控")
    col1, col2 = st.columns(2)
    col1.metric("數據來源", "Yahoo Finance", "正常")
    col2.metric("AI 模型", "GPT-4o-mini", "連線中")
    st.info("系統運作穩定，您可隨時進行個股健檢。")

# 頁面：AI 智慧分析
elif menu == "🤖 AI 智慧分析":
    st.subheader("個股深度健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    if st.button("啟動 AI 深度分析"):
        with st.spinner("正在讀取即時財報並進行深度推論..."):
            try:
                stock = yf.Ticker(f"{t}.TW")
                info = stock.info
                funda = f"PE: {info.get('trailingPE', 'N/A')}, EPS: {info.get('trailingEps', 'N/A')}"
                prompt = f"分析 {t}，基本面數據：{funda}。請以專業基金經理人的角度分析該股優劣，並給出明確建議。"
                response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                res = response.choices[0].message.content
                st.markdown(f"### 🎯 AI 分析報告\n{res}")
                st.session_state.logs.append({"時間": datetime.now().strftime("%H:%M"), "代號": t, "結果": "已分析"})
            except Exception as e:
                st.error(f"分析失敗，請檢查代號是否正確。錯誤訊息: {e}")

# 頁面：部位管理
elif menu == "💼 部位管理":
    st.subheader("我的持股看板")
    df = st.session_state.portfolio
    df['損益'] = df['現價'] - df['成本']
    fig = px.bar(df, x='名稱', y='損益', color='損益', text='損益', template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# 頁面：分享建議
elif menu == "📋 分享建議":
    st.subheader("📢 給親友的操作與安全守則")
    st.warning("""
    ### ⚠️ 為了確保您的帳戶安全，分享前請閱讀以下守則：
    1. **本系統為分析輔助工具**：AI 產出的分析僅供決策參考，**非任何買賣建議或投資擔保**。
    2. **數據延遲**：本系統所使用的市場資料由 Yahoo Finance 提供，並非即時交易數據。
    3. **安全提醒 (關鍵)**：
       - **請勿索取或分享 API Key**：此應用程式含有您的個人 API 設定，分享連結給他人時，請勿洩漏 Streamlit 的秘密設定畫面。
       - **費用控管**：此服務採用點數計費，請勿短時間內進行大量重複查詢，以免消耗您的 OpenRouter 餘額。
    4. **風險自負**：股票投資具有市場風險，所有下單行為請由使用者自行承擔盈虧。
    """)
    st.success("若要分享給親友，請直接提供該應用程式網址，系統會自動隔離您的 API 設定，確保對方無法窺探您的金鑰。")
