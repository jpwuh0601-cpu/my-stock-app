import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 增強版路徑讀取：檢查多個可能路徑
def load_data():
    # 嘗試多個路徑：當前目錄、專案根目錄、以及 Streamlit 預設掛載目錄
    possible_paths = [
        "market_data.json",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json"),
        "/mount/src/my-stock-app/market_data.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                continue
    return None

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼")

if st.sidebar.button("開始搜尋"):
    if data:
        # 強制讀取預設值避免 metric 報錯
        price = str(data.get("price", "-"))
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", price)
        # ... (其餘 UI 邏輯)
        st.success("資料讀取成功！")
    else:
        st.error("找不到市場資料檔 (market_data.json)。")
        # 除錯顯示
        st.write("目前路徑:", os.getcwd())
        st.write("目錄內檔案:", os.listdir('.'))

else:
    st.info("請按下搜尋按鈕。")
