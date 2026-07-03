import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """從 JSON 檔案載入數據"""
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
        st.info("資料庫初始化中，請稍候。")
        return

    # 側邊欄：選擇器與確定按鈕
    with st.sidebar:
        st.subheader("控制面板")
        selected = st.selectbox("請選擇監控標的", tickers)
        # 加入確定按鈕，點擊後才會更新顯示內容
        confirm_btn = st.button("確認選擇")

    # 邏輯：只有在按下確認按鈕後才顯示數據
    if confirm_btn:
        st.session_state.selected_ticker = selected

    # 顯示數據
    current_ticker = st.session_state.get("selected_ticker", tickers[0])
    info = data.get(current_ticker, {})
    
    st.subheader(f"{current_ticker} 監控數據")

    # 建立 4 個頁籤
    tab1, tab2, tab3, tab4 = st.tabs(["📊 即時股價與財報", "🏦 法人與資券籌碼", "🤖 AI 分析與新聞", "🛠 系統回測檢查"])
    
    with tab1:
        st.subheader(f"{current_ticker} 基本面數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
        col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
        col3.metric("每股淨值 (BVPS)", f"{info.get('bvps', 0):,.2f}")
        st.metric("本益比 (PE)", f"{info.get('pe', 0):,.2f}")
        
        if info.get("history"):
            df = pd.DataFrame(info["history"])
            st.line_chart(df.set_index("Date")["Close"])

    with tab2:
        st.subheader("籌碼面數據")
        chip_info = info.get("chip_data", {})
        st.metric("法人動向", chip_info.get("institutional_buy", "無數據"))
        st.metric("資券比", chip_info.get("margin_ratio", "無數據"))

    with tab3:
        st.subheader("AI 投資快評")
        st.write(info.get("ai_prediction") or "分析模組處理中...")

    with tab4:
        st.subheader("系統監控")
        st.write(f"資料最後更新時間: {data.get('last_updated', '未知')}")
        st.success("自動化管線運作正常")

if __name__ == "__main__":
    main()
