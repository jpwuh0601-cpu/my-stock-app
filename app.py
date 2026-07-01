import streamlit as st
import json
import os
import pandas as pd
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式 (增強版)
def load_data():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    
    if not os.path.exists(json_path):
        return None, f"找不到檔案: {json_path}"
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return None, "檔案為空"
            data = json.loads(content)
            return data, None
    except Exception as e:
        return None, f"解析失敗: {str(e)}"

# 初始化資料
data, error_msg = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 1301)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 顯示資料 (原邏輯)
        col1, col2, col3, col4 = st.columns(4)
        
        # 使用 .get() 確保不會因為缺欄位而報錯
        price = data.get("price", "N/A")
        bvps = data.get("bvps", "N/A")
        
        col1.metric("即時股價", str(price))
        col2.metric("每股淨值", str(bvps))
        
        # ... (其餘邏輯)
        st.success("數據載入成功")
    else:
        st.error(f"數據讀取失敗: {error_msg}")
        st.warning("請確認 GitHub Actions 是否成功寫入 market_data.json，或是檔案格式是否正確。")
        if data:
            st.write("已讀取到的數據內容:", data)
else:
    if error_msg:
        st.info(f"系統訊息: {error_msg}")
    st.info("請輸入代碼後按下搜尋。")
