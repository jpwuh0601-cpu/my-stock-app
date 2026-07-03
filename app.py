import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 強制指向程式所在目錄，讀取正確的 JSON 檔案
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
    
    # 提取所有股票代號，確保移除 last_updated
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請稍候。")
        return

    # 初始化 session_state，確保選股狀態被記憶
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0]

    # 側邊欄設計：監聽選單變更
    with st.sidebar:
        st.subheader("控制面板")
        
        # 顯示下拉選單
        current_selection = st.selectbox(
            "請選擇監控標的", 
            tickers, 
            index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0
        )
        
        # 透過按鈕強制更新 session 並觸發重新渲染
        if st.button("確認選擇"):
            if st.session_state.selected_ticker != current_selection:
                st.session_state.selected_ticker = current_selection
                st.rerun() # 強制刷新介面，讓儀表板讀取新股票數據

    # 根據選定的代號取出對應的數據
    info = data.get(st.session_state.selected_ticker, {})
    
    st.subheader(f"{st.session_state.selected_ticker} 即時財報")
    
    # 顯示數據
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
    col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
    col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
    
    st.info(f"AI 分析快評: {info.get('ai_prediction', '分析中...')}")
    st.write(f"系統最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
