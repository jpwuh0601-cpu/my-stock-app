import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="金融智慧終端")

def main():
    st.title("📈 專業金融智慧監控系統")
    
    # 1. 初始化 session_state 用於儲存觀察名單
    if 'my_tickers' not in st.session_state:
        st.session_state.my_tickers = ["2330.TW", "2317.TW"]

    # 2. 自選股票管理介面
    with st.sidebar.expander("管理我的自選股"):
        new_ticker = st.text_input("新增股票 (例: 2454.TW)")
        if st.button("確認加入"):
            if new_ticker and new_ticker not in st.session_state.my_tickers:
                st.session_state.my_tickers.append(new_ticker)
        
        st.write("目前清單:", st.session_state.my_tickers)

    # 3. 讀取市場數據
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        st.warning("請等待自動化排程同步市場數據...")
        return

    # 4. 股票選擇器
    target = st.selectbox("選擇要分析的股票", st.session_state.my_tickers)
    
    if target in data:
        info = data[target]
        # ... (後續顯示邏輯與之前相同)
        st.success(f"正在分析: {target}")
        col1, col2, col3 = st.columns(3)
        col1.metric("EPS", info.get('eps', 0))
        col2.metric("本益比", info.get('pe', 0))
        col3.metric("每股淨值", info.get('nav', 0))
        # ...
    else:
        st.error(f"找不到 {target} 的數據，請確認該股票是否在後端監控列表中。")

if __name__ == "__main__":
    main()
