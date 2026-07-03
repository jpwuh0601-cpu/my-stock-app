import streamlit as st
import pandas as pd
import json
import os # 務必確保匯入 os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 搜尋設定
    with st.sidebar:
        st.subheader("搜尋設定")
        user_input = st.text_input("輸入股票代號 (如: 6770.TW)")
        if st.button("確定選股"):
            st.session_state.target = user_input

    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    if info:
        st.markdown(f"## {target} 即時股價: :{ 'red' if info.get('change',0)>=0 else 'green' }[{info.get('price', 0):,.2f}]")
        
        st.subheader("三大法人 10 日每日張數細項")
        st.dataframe(pd.DataFrame(info.get("institutional_daily", [])), use_container_width=True)
        
        st.subheader("10 家主力券商 10 日每日張數細項")
        st.dataframe(pd.DataFrame(info.get("broker_daily", [])), use_container_width=True)
    else:
        st.warning("查無此股票資料，請確保代號已加入 worker.py 並執行過 GitHub Action。")

if __name__ == "__main__":
    main()
