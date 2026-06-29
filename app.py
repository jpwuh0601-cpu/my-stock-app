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
    # 呈現即時股價與每股淨值
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"{data['price']}", delta=f"{data['change']}%")
    col2.metric("每股淨值 (BVPS)", f"{data['bvps']}")

    # 呈現法人買賣超
    st.subheader("🏢 三大法人買賣超")
    df_inst = pd.DataFrame(data['institutional_investors'])
    st.table(df_inst)

    # 呈現 AI 預測與新聞
    st.subheader("📰 市場動態與 AI 預測")
    st.info(f"**AI 預測**: {data['ai_prediction']}")
    st.write("**最新新聞**:", data['news'])

else:
    st.warning("請執行自動化任務以載入數據。")
