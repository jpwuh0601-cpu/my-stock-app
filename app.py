import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]

    # 選股介面
    with st.sidebar:
        st.subheader("搜尋設定")
        user_input = st.text_input("輸入股票代號 (例如: 2330.TW)", key="input")
        # 加入「確定」按鈕
        if st.button("確定搜尋"):
            st.session_state.target = user_input
    
    # 邏輯設定
    target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(target, {})

    if info:
        st.markdown(f"## {target} 即時股價: :{ 'red' if info.get('change',0)>=0 else 'green' }[{info.get('price', 0):,.2f}]")
        
        # 三大法人每日詳細表格
        st.subheader("三大法人 10 日每日張數細項")
        st.dataframe(pd.DataFrame(info.get("institutional_daily", [])), use_container_width=True)
        
        # 10家券商每日詳細表格
        st.subheader("10 家主力券商每日張數細項")
        st.dataframe(pd.DataFrame(info.get("broker_daily", [])), use_container_width=True)
    else:
        st.warning("查無此股票或數據尚未更新，請輸入正確代號並點擊確定。")

if __name__ == "__main__":
    main()
