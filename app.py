import streamlit as st
import json
import os

st.set_page_config(page_title="AI 投資秘書儀表板", layout="wide")

# 增加緩存機制，避免讀取檔案造成無窮重載
@st.cache_data(ttl=60)
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

st.title("📈 AI 投資秘書儀表板")

data = load_data()

if data:
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇分析個股", tickers)
    
    ticker_data = data.get(selected_ticker, {})
    st.header(f"個股分析: {selected_ticker}")
    
    # 簡化顯示，避免複雜邏輯觸發錯誤
    st.metric("目前價格", ticker_data.get('price', '資料載入中...'))
    
    st.subheader("🤖 AI 深度分析")
    st.markdown(ticker_data.get('ai_report', '分析生成中...'))
else:
    st.warning("系統正在初始化數據，請稍候。若畫面持續載入，請確認 GitHub Actions 是否已成功產生 market_data.json。")
