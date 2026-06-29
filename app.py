import streamlit as st
import json
import os

st.set_page_config(page_title="AI 投資決策儀表板", layout="wide")
st.title("📊 AI 投資決策儀表板")

def load_data():
    # 強制指定讀取 market_data.json
    file_path = "market_data.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

if data:
    # 顯示數據
    st.metric("即時股價", f"{data['price']}", delta=f"{data['change']}%")
    st.json(data) # 先用 json 確認數據正確呈現
else:
    st.error("找不到 market_data.json，請檢查自動化任務執行狀態。")
