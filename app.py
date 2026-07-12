import streamlit as st
import json
import os
import sys

# 頁面配置
st.set_page_config(page_title="股市儀表板", layout="wide")
st.title("📈 股市決策儀表板")

# 環境檢測與資料讀取
st.sidebar.write(f"Python 版本: {sys.version.split()[0]}")

try:
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    ticker = st.selectbox("請選擇股票", list(data.keys()))
    if ticker:
        d = data[ticker]
        # 顯示區
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("股價", d.get("price", 0))
        col2.metric("每股淨值", d.get("nav", 0))
        col3.metric("本益比", d.get("pe", 0))
        col4.metric("EPS", d.get("eps", 0))
        
        # 財務預估區
        st.subheader("📊 財務預估模型")
        st.write("已成功載入數據")
except Exception as e:
    st.error(f"系統錯誤: {e}")
    st.info("若錯誤顯示為 module not found，請刪除 App 後重新部署，並確保 requirements.txt 檔案名稱正確無誤。")
