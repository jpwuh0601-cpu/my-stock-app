import streamlit as st
import json
import os

st.set_page_config(page_title="AI 股票分析看板", layout="wide")

# CSS 優化：加入卡片陰影與顏色標示
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    .buy-signal { color: #28a745; font-weight: bold; }
    .sell-signal { color: #dc3545; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_market_data():
    if not os.path.exists('market_data.json'):
        return {}
    try:
        with open('market_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

st.title("📈 AI 實戰選股看板")

data = load_market_data()

if not data:
    st.warning("⚠️ 數據庫更新中，請稍候...")
else:
    tickers = list(data.keys())
    selected = st.selectbox("請選擇目標股票", tickers)
    stock = data.get(selected, {})

    # 頂部卡片區
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("股價", f"{stock.get('price', 0)}")
    
    # PE/EPS 顏色與邏輯處理
    pe = stock.get('pe', 0)
    col2.metric("本益比 (PE)", pe, delta_color="normal")
    col3.metric("每股盈餘 (EPS)", stock.get('eps', 0))
    
    # 安全等級標示
    level = stock.get('black_swan', '未知')
    col4.markdown(f"**安全等級**<br>{'🟢' if level == '安全' else '🔴'} {level}", unsafe_allow_html=True)

    # AI 決策卡片
    prediction = stock.get('ai_prediction', '')
    st.markdown("### 🤖 AI 決策分析")
    
    # 根據內容上色
    if "積極買入" in prediction:
        st.markdown(f"<div style='border:2px solid #28a745; padding:15px; border-radius:10px;'><h3 class='buy-signal'>🚀 {prediction}</h3></div>", unsafe_allow_html=True)
    elif "減碼" in prediction:
        st.markdown(f"<div style='border:2px solid #dc3545; padding:15px; border-radius:10px;'><h3 class='sell-signal'>⚠️ {prediction}</h3></div>", unsafe_allow_html=True)
    else:
        st.info(prediction)

    st.markdown("---")
    st.write(f"📰 最新市場資訊: {stock.get('news', '暫無更新')}")
