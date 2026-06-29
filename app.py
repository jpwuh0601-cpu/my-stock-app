import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="AI 投資決策儀表板", layout="wide")

st.title("📊 AI 投資決策儀表板")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

if data:
    # 建立三個分頁
    tab1, tab2, tab3 = st.tabs(["市場概況", "法人籌碼", "AI 分析"])
    
    with tab1:
        col1, col2 = st.columns(2)
        col1.metric("即時股價", f"{data['price']}", delta=f"{data['change']}%")
        col2.metric("每股淨值 (BVPS)", f"{data['bvps']}")
        st.write("最新新聞:", data['news'])

    with tab2:
        st.subheader("三大法人籌碼分析")
        df = pd.DataFrame(data['institutional_investors'])
        st.table(df)
        
    with tab3:
        st.subheader("AI 深度分析")
        st.info(data['ai_prediction'])

else:
    st.warning("尚未載入數據，請稍候自動化任務執行。")
