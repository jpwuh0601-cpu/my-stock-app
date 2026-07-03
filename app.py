import streamlit as st
import pandas as pd
import json
import os

# 設定頁面
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    # 使用當前工作目錄
    path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("資料載入中或數據庫為空...")
        return

    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        target = st.selectbox("選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
    
    target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(target, {})

    if info:
        st.subheader(f"分析目標: {target}")
        
        # 修正：將 use_container_width 替換為 width='stretch'
        if "institutional_daily" in info:
            st.subheader("三大法人 10 日買賣超")
            st.dataframe(pd.DataFrame(info["institutional_daily"]), width=None) # 預設自動適應寬度
            
        if "broker_daily" in info:
            st.subheader("主力券商 10 日買賣超")
            st.dataframe(pd.DataFrame(info["broker_daily"]), width=None)
    else:
        st.write("請從側邊欄搜尋並點擊選股。")

if __name__ == "__main__":
    main()
