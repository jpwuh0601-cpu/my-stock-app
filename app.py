import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 設定與 worker.py 一致的數據路徑
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
    
    # 提取所有股票代號
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請稍候。")
        return

    # 初始化選股狀態
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0]

    # 側邊欄：選股機制
    with st.sidebar:
        st.subheader("控制面板")
        # 綁定選單變更
        current_selection = st.selectbox(
            "請選擇監控標的", 
            tickers, 
            index=tickers.index(st.session_state.selected_ticker)
        )
        
        if st.button("確認選擇"):
            if st.session_state.selected_ticker != current_selection:
                st.session_state.selected_ticker = current_selection
                st.rerun()  # 強制重新渲染頁面

    # 顯示數據
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
