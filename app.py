import streamlit as st
import json
import os

st.set_page_config(page_title="AI 股票籌碼看板", layout="wide")

@st.cache_data(ttl=3600)
def load_market_data():
    if not os.path.exists('market_data.json'):
        return {}
    try:
        with open('market_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

st.title("📈 AI 籌碼實戰分析看板")

data = load_market_data()

if not data:
    st.warning("⚠️ 數據庫更新中，請稍候...")
else:
    tickers = list(data.keys())
    selected = st.selectbox("請選擇目標股票", tickers)
    stock = data.get(selected, {})

    # 1. 核心指標區
    col1, col2, col3 = st.columns(3)
    col1.metric("當前股價", f"{stock.get('price', 0)}")
    col2.metric("本益比 (PE)", f"{stock.get('pe', 0)}")
    col3.metric("每股盈餘 (EPS)", f"{stock.get('eps', 0)}")

    # 2. 籌碼面視覺化 (institutional_data 呈現)
    st.markdown("### 🏛️ 機構籌碼流向")
    inst_data = stock.get('institutional_data', [])
    if inst_data:
        latest = inst_data[0]
        st.write(f"日期: {latest.get('日期')} | 外資持有量: {latest.get('外資', 0):,.0f}")
        # 使用進度條顯示相對強度
        st.progress(min(latest.get('外資', 0) / 1000000, 1.0))
    
    # 3. AI 分析決策區
    st.markdown("### 🤖 AI 決策觀點")
    prediction = stock.get('ai_prediction', '暫無分析')
    st.info(prediction)
