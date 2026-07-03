import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請等待 GitHub Actions 自動更新...")
        return

    # 側邊欄設計
    with st.sidebar:
        selected = st.selectbox("請選擇監控標的", tickers)
        if st.button("確認選擇"):
            st.session_state.selected_ticker = selected

    current_ticker = st.session_state.get("selected_ticker", tickers[0])
    info = data.get(current_ticker, {})

    # 判斷是否為初始狀態 (price 為 0)
    if info.get("price", 0) == 0:
        st.warning(f"{current_ticker} 尚未完成資料抓取，請稍候。")
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 即時股價與財報", "🏦 法人與資券籌碼", "🤖 AI 分析與新聞", "🛠 系統回測檢查"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
            col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
            col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
        
        with tab2:
            chip = info.get("chip_data", {})
            st.write(f"法人動向: {chip.get('institutional_buy', '暫無數據')}")
            
        with tab3:
            st.write(info.get("ai_prediction", "AI 分析進行中..."))

        with tab4:
            st.success(f"資料最後更新時間: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
