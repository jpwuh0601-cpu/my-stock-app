import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="專業金融監控終端")

def load_data():
    if not os.path.exists("market_data.json"): return {}
    try:
        with open("market_data.json", "r", encoding="utf-8") as f: 
            return json.load(f)
    except: return {}

def main():
    st.title("📈 專業金融監控終端")
    data = load_data()
    
    if not data:
        st.error("系統資料庫目前為空。")
        return

    # 1. 側邊欄過濾與選股
    with st.sidebar:
        valid_tickers = list(data.keys())
        selected = st.selectbox("選擇監控股票", valid_tickers)
        if st.button("確認選股"):
            st.session_state.target = selected
            st.rerun()

    target = st.session_state.get("target", valid_tickers[0])
    info = data.get(target, {})

    # 2. 防禦性渲染：使用 .get() 並提供明確預設值
    st.metric("即時股價", f"{info.get('price', 0)} 元", delta=str(info.get('change', 0)))

    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值", str(info.get('nav', 'N/A')))
    c2.metric("本益比", str(info.get('pe', 'N/A')))
    c3.metric("EPS", str(info.get('eps', 'N/A')))

    st.subheader("籌碼面資料")
    inst = info.get('institutional_data', [])
    if inst:
        st.dataframe(pd.DataFrame(inst), use_container_width=True)
    else:
        st.info("尚無籌碼數據")

if __name__ == "__main__":
    main()
