import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if not os.path.exists("market_data.json"):
        return {}
    with open("market_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("系統數據載入中，請確保 GitHub Action 已成功執行。")
        return

    # 側邊欄：搜尋與選股
    with st.sidebar:
        user_input = st.text_input("輸入股票代號 (例如: 6770.TW)")
        if st.button("確定選股"):
            st.session_state.target = user_input
    
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    if info:
        # 即時股價與色彩標示
        chg = info.get("change", 0)
        st.markdown(f"## {target} 即時股價: :{ 'red' if chg>=0 else 'green' }[{info.get('price', 0):,.2f}]")
        
        # 三大法人表格
        st.subheader("三大法人 10 日買賣超細項")
        st.dataframe(pd.DataFrame(info.get("institutional_daily", [])), use_container_width=True)
        
        # 10 家券商表格
        st.subheader("10 家主力券商 10 日買賣超細項")
        st.dataframe(pd.DataFrame(info.get("broker_daily", [])), use_container_width=True)
    else:
        st.warning(f"查無 {target} 之資料。")

if __name__ == "__main__":
    main()
