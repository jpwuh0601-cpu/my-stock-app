import streamlit as st
import json
import os

# 在使用 pandas 前先進行安裝檢查
try:
    import pandas as pd
except ImportError:
    st.error("系統錯誤：套件 'pandas' 未安裝，請確認 requirements.txt 已正確提交。")
    st.stop()

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f), None
    return None, f"找不到資料檔: {file_path}"

def main():
    st.title("📈 AI 智能金融監控終端")
    
    data, error = load_data()
    if error:
        st.error(error)
        return

    tickers = [t for t in data.keys() if t != "last_updated"]
    
    # 側邊欄選股
    with st.sidebar:
        st.subheader("選股搜尋")
        target = st.selectbox("請選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    info = data.get(target, {})
    st.subheader(f"目標股票: {target}")
    
    # 這裡現在可以放心使用 pd，因為已經檢查過 import 了
    if "institutional_daily" in info:
        st.subheader("三大法人細項")
        st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)

if __name__ == "__main__":
    main()
