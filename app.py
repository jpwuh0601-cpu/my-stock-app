import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 自由選股儀表板")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📊 AI 自由選股金融終端")
    data = load_data()

    # 側邊欄：除了選擇，增加一個文字輸入框，讓您輸入新股票
    with st.sidebar:
        st.subheader("選股控制台")
        
        # 顯示既有清單
        current_tickers = [t for t in data.keys() if t != "last_updated"]
        selected = st.selectbox("1. 選擇監控中股票", current_tickers)
        
        # 讓用戶手動輸入新股票
        new_ticker = st.text_input("2. 輸入新股票代號 (例如: 2317.TW)")
        if st.button("加入監控/查看") and new_ticker:
            st.session_state.target = new_ticker
            st.rerun()

    sym = st.session_state.get("target", selected if selected else "2330.TW")
    info = data.get(sym, {})

    st.header(f"股票: {sym}")
    
    # 即時股價與漲跌
    diff = info.get("diff", 0)
    st.metric("即時股價", info.get("price", "請等待更新"), delta=f"{diff} 元")

    # 籌碼顯示
    st.subheader("5. 三大法人買賣超細項")
    if "institutional_daily" in info:
        st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
    else:
        st.info("該股票數據尚未同步，請等待 worker.py 完成抓取。")

    st.subheader("6. 主力券商買賣超細項")
    if "broker_daily" in info:
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)

    st.subheader("7. AI 深度分析")
    st.success(info.get("ai_prediction", "AI 正在分析此股票..."))

if __name__ == "__main__":
    main()
