import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 確保路徑讀取與 GitHub 的 market_data.json 一致
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 排除更新時間，只取股票代號
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫讀取中，若畫面未更新請稍候...")
        return

    # 使用 session_state 來持久化當前選擇，確保選單變更時能精準更新畫面
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0]

    with st.sidebar:
        st.subheader("控制面板")
        # 將目前的選項綁定到 session_state
        selected = st.selectbox(
            "監控標的", 
            tickers, 
            index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0
        )
        
        if st.button("確認選擇"):
            # 只有在選擇確實改變時才觸發 rerun
            if st.session_state.selected_ticker != selected:
                st.session_state.selected_ticker = selected
                st.rerun()

    # 顯示數據區域
    info = data.get(st.session_state.selected_ticker, {})
    
    st.subheader(f"{st.session_state.selected_ticker} 即時財報")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
    col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
    col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
    
    st.info(f"AI 分析快評: {info.get('ai_prediction', '分析中...')}")
    st.write(f"系統最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
