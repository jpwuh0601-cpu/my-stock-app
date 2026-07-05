import streamlit as st
import json
import os
import time

st.set_page_config(page_title="AI 投資秘書儀表板", layout="wide")

# 強制讀取檔案，並清除快取以避免舊數據殘留
@st.cache_data(ttl=1) # 設定快取時間為 1 秒，強制每次重新載入
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            return {"error": str(e)}
    return None

st.title("📈 AI 投資秘書儀表板")

data = load_data()

# 顯示數據時間戳記，幫助確認資料是否為最新
if os.path.exists("market_data.json"):
    last_modified = time.ctime(os.path.getmtime("market_data.json"))
    st.caption(f"數據最後更新時間: {last_modified}")

if data and "error" not in data:
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇分析個股", tickers)
    
    ticker_data = data.get(selected_ticker, {})
    st.header(f"個股分析: {selected_ticker}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("目前價格", ticker_data.get('price', '資料載入中...'))
        
    st.subheader("🤖 AI 深度分析")
    st.markdown(ticker_data.get('ai_report', '分析生成中...'))
else:
    st.warning("數據更新中，請稍候。如果持續看不到數據，請確認 GitHub Actions 是否執行成功。")
