import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 強制指向程式所在目錄，確保讀寫同一檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """從 JSON 檔案載入數據"""
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
    
    # 提取所有股票代號 (排除最後更新時間)
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請等待 GitHub Actions 自動更新...")
        return

    # 初始化 session_state
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0]

    # 側邊欄設計
    with st.sidebar:
        st.subheader("控制面板")
        # 建立選單
        selected = st.selectbox(
            "請選擇監控標的", 
            tickers, 
            index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0
        )
        
        # 綁定確認按鈕來觸發頁面刷新
        if st.button("確認選擇"):
            if st.session_state.selected_ticker != selected:
                st.session_state.selected_ticker = selected
                st.rerun()

    # 取得當前選擇的股票數據
    current_ticker = st.session_state.selected_ticker
    info = data.get(current_ticker, {})

    # 顯示該選定標的的數據
    st.subheader(f"{current_ticker} 即時財報")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
    col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
    col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
    
    st.info(f"AI 分析快評: {info.get('ai_prediction', '分析中...')}")
    st.write(f"系統最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
