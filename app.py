import streamlit as st
import json
import os
import pandas as pd

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 強制將路徑設定為程式所在的根目錄，確保讀寫同一檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """從程式目錄載入 JSON 數據"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception as e:
                st.error(f"讀取資料失敗: {e}")
                return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 過濾掉 last_updated 欄位，只留下股票代號
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請等待 GitHub Actions 自動更新 (目前找不到有效標的)...")
        return

    # 側邊欄設計
    with st.sidebar:
        st.subheader("控制面板")
        selected = st.selectbox("請選擇監控標的", tickers)
        if st.button("確認選擇"):
            st.session_state.selected_ticker = selected

    # 取得當前選擇的股票資訊
    current_ticker = st.session_state.get("selected_ticker", tickers[0])
    info = data.get(current_ticker, {})

    # 顯示數據 (檢查是否為 0 表示未更新)
    if info.get("price", 0) == 0:
        st.warning(f"{current_ticker} 目前無有效數據，請確認自動化任務是否已執行。")
    else:
        st.subheader(f"{current_ticker} 監控數據")
        tab1, tab2, tab3, tab4 = st.tabs(["📊 即時股價與財報", "🏦 法人與資券籌碼", "🤖 AI 分析與新聞", "🛠 系統回測檢查"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
            col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
            col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
        
        with tab2:
            st.write("法人動向與資券比數據已準備就緒。")
            
        with tab3:
            st.write(info.get("ai_prediction", "AI 分析進行中..."))

        with tab4:
            st.success(f"資料最後更新時間: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
