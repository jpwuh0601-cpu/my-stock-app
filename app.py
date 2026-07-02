import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 強制路徑指向根目錄
file_path = os.path.join(os.getcwd(), "market_data.json")

def load_data():
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

data = load_data()

st.title("📊 AI 智能投資決策儀表板")

if data is None:
    st.warning("⚠️ 系統載入中，請確認 GitHub Actions (Daily Stock Analysis) 已執行，或稍後重試。")
else:
    # 渲染指標
    cols = st.columns(6)
    cols[0].metric("股價", f"{data.get('price', 0):,.2f}")
    
    # 渲染表格 (加入檢查)
    if "top_brokers" in data:
        st.subheader("10日主力券商")
        st.dataframe(pd.DataFrame(data["top_brokers"]))
