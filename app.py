import streamlit as st
from worker import fetch_stock_data
import pandas as pd

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 1. 輸入與查詢邏輯
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取資料..."):
        # 呼叫 worker.py 中的 fetch_stock_data
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error(data["error"])
        else:
            # 2. 顯示股價指標
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['price']:.2f}")
            col2.metric("每股淨值", f"{data['nav']:.2f}")
            col3.metric("本益比", f"{data['pe']:.2f}")
            col4.metric("EPS", f"{data['eps']:.2f}")
            
            # 3. 顯示法人籌碼數據 (來自 worker.py 生成的 DataFrame)
            if "institutional_data" in data:
                st.markdown("### 📊 法人近期買賣超明細 (張)")
                st.dataframe(data["institutional_data"], use_container_width=True)
            
            st.success(f"代號 {ticker} 數據分析完成！")
else:
    st.info("請在左側輸入股票代號並點擊「查詢分析數據」。")
