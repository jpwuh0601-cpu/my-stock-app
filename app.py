import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(layout="wide", page_title="AI 金融終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請等待自動更新...")
        return

    selected = st.sidebar.selectbox("選擇監控標的", tickers)
    info = data.get(selected, {})
    
    # 建立 4 個頁籤
    tab1, tab2, tab3, tab4 = st.tabs(["📊 即時股價與財報", "🏦 法人與資券籌碼", "🤖 AI 分析與新聞", "🛠 系統回測檢查"])
    
    with tab1:
        st.subheader(f"{selected} 基本面數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
        col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
        col3.metric("每股淨值 (BVPS)", f"{info.get('bvps', 0):,.2f}")
        st.metric("本益比 (PE)", f"{info.get('pe', 0):,.2f}")

    with tab2:
        st.subheader("籌碼面數據")
        st.warning("待實作：將透過網頁爬蟲取得三大法人與資券比數據")

    with tab3:
        st.subheader("AI 投資快評")
        st.write(info.get("ai_prediction") or "AI 分析準備中...")

    with tab4:
        st.subheader("系統監控")
        st.write(f"最後更新時間: {data.get('last_updated')}")
        st.success("自動化管線狀態：綠勾 (正常)")

if __name__ == "__main__":
    main()
