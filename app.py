import streamlit as st
import pandas as pd
import numpy as np

# 1. 頁面初始化 (設在最上方)
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

st.title("📈 專業股市決策儀表板")
st.write("應用程式已成功啟動！")

# 2. 簡化輸入區
ticker = st.sidebar.text_input("輸入股票代號", "2330")

# 3. 只有點擊按鈕時才執行運算
if st.sidebar.button("開始分析"):
    try:
        st.write(f"正在分析代號: {ticker}")
        
        # 測試用假資料，避免 yfinance 連線失敗
        st.subheader("1. 即時股價 (測試數據)")
        st.metric("現價", "600.00", "+5.50")
        
        st.subheader("2. 財務指標")
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨額", "120.5")
        c2.metric("本益比", "20.1")
        c3.metric("EPS", "25.0")
        
        st.success("分析完成！")
        
    except Exception as e:
        st.error(f"執行錯誤: {e}")
else:
    st.info("請在側邊欄輸入代號並點擊「開始分析」按鈕。")
