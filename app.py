import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

def load_data():
    # 定義可能的搜尋路徑
    possible_paths = [
        "market_data.json",                                # 當前目錄
        "/mount/src/my-stock-app/market_data.json",        # Streamlit 雲端路徑
        os.path.join(os.getcwd(), "market_data.json"),      # 工作目錄
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f), path # 回傳資料與路徑
            except Exception:
                continue
    return None, None

data, used_path = load_data()

if data is None:
    st.error("⚠️ 找不到 market_data.json")
    st.write("目前工作目錄:", os.getcwd())
    st.write("目錄內容:", os.listdir('.'))
else:
    st.success(f"✅ 資料來源: {used_path}")
    
    # 接下來顯示資料
    price = str(data.get("price", "-"))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("即時股價", price)
    # ... (其餘 UI 邏輯)
