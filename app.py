import streamlit as st
import json
import os
import pandas as pd

# 設定頁面配置
st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.title("📈 AI 專業金融分析終端")
    
    # 載入數據
    data = load_data("market_data.json")
    
    # --- 自選股票側邊欄 ---
    with st.sidebar:
        st.header("自選股票管理")
        # 顯示目前的數據庫中有哪些股票
        available_tickers = list(data.keys()) if data else []
        selected_ticker = st.selectbox("從現有監控清單選擇：", available_tickers)
        
        # 自定義輸入區
        custom_input = st.text_input("輸入新股票代號 (例如: 2317.TW)")
        
        if st.button("確認選股"):
            target = custom_input if custom_input else selected_ticker
            st.session_state.target = target
            st.rerun()

    # 取得當前目標
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target)

    # 顯示主頁資訊
    if not info:
        st.warning(f"⚠️ 找不到 {target} 的資料。若您剛輸入，請等待 GitHub Actions 更新或檢查代號是否正確。")
        return

    st.header(f"監控標的: {target}")
    
    # 核心指標
    c1, c2, c3 = st.columns(3)
    c1.metric("當前價格", f"{info.get('price', 0)} 元")
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    st.subheader("AI 分析")
    st.write(info.get('ai_prediction', '分析中...'))

if __name__ == "__main__":
    main()
