import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="AI 投資儀表板", layout="wide")
st.title("📊 AI 投資決策儀表板")

try:
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    col1, col2 = st.columns(2)
    col1.metric("即時股價", f"{data['price']}", f"{data['change']}%")
    col2.metric("每股淨值 (BVPS)", f"{data['bvps']}")
    
    st.subheader("三大法人買賣超")
    st.table(pd.DataFrame(data['institutional_investors']))
    
    st.subheader("AI 深度分析")
    st.info(data['ai_prediction'])
except FileNotFoundError:
    st.error("數據檔案尚未產出，請檢查 GitHub Actions 狀態。")
