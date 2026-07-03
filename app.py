import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

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

def check_system_health(last_update_str):
    """檢查數據是否過舊 (超過 26 小時視為異常)"""
    try:
        last_update = datetime.strptime(last_update_str, "%Y-%m-%d %H:%M:%S")
        diff = datetime.now() - last_update
        return diff.total_seconds() < 26 * 3600
    except:
        return False

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("資料庫初始化中，請稍候。")
        return

    # 系統健康檢查
    is_healthy = check_system_health(data.get("last_updated", ""))
    
    with st.sidebar:
        st.subheader("控制面板")
        selected = st.selectbox("請選擇監控標的", tickers)
        confirm_btn = st.button("確認選擇")
        
        st.divider()
        st.subheader("系統狀態")
        if is_healthy:
            st.success("自動化管線運作正常 (數據新鮮)")
        else:
            st.error("警告：系統資料已過時，請檢查 GitHub Actions")

    if confirm_btn:
        st.session_state.selected_ticker = selected

    current_ticker = st.session_state.get("selected_ticker", tickers[0])
    info = data.get(current_ticker, {})
    
    st.subheader(f"{current_ticker} 監控數據")

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
        if is_healthy:
            st.success("系統狀態：良好")
        else:
            st.error("系統狀態：數據已過期，請檢查自動化任務執行紀錄")

if __name__ == "__main__":
    main()
