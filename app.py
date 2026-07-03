import streamlit as st
import json
import os

# 設定頁面
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 獲取路徑
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
    
    # 載入數據
    data = load_data()
    # 過濾標的，確保只有股票代號
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫讀取中，請稍候...")
        return

    # 使用 session_state 記憶選股
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0]

    # 側邊欄 UI
    with st.sidebar:
        st.subheader("控制面板")
        
        # 選單設定
        selected = st.selectbox(
            "選擇標的", 
            tickers, 
            index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0
        )
        
        # 按鈕同步邏輯
        if st.button("確認選擇"):
            if st.session_state.selected_ticker != selected:
                st.session_state.selected_ticker = selected
                st.rerun() # 強制讓頁面重繪，更新顯示數值

    # 取得選定數據
    current_ticker = st.session_state.selected_ticker
    info = data.get(current_ticker, {})
    
    # 顯示數據
    st.header(f"監控標的: {current_ticker}")
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
    col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
    col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
    
    st.info(f"AI 分析: {info.get('ai_prediction', '無數據')}")
    st.caption(f"最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
