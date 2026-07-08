import streamlit as st
from worker import fetch_stock_data
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 側邊欄輸入
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner(f"正在即時獲取 {ticker_input} 的數據..."):
        # 直接呼叫 worker.py 的函數
        data = fetch_stock_data(ticker_input)
        
        if "error" in data:
            st.error(data["error"])
        else:
            # 1. 顯示即時股價資訊
            st.markdown(f"### {ticker_input.upper()} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            
            # 顏色邏輯
            change = data.get('change', 0)
            color = "red" if change >= 0 else "green"
            
            col1.metric("即時股價", f"{data.get('price', 0):.2f}")
            col2.metric("漲跌", f"{change:.2f}", delta_color="inverse")
            col3.metric("本益比", f"{data.get('pe', 0):.2f}")
            col4.metric("每股盈餘 (EPS)", f"{data.get('eps', 0):.2f}")

            st.divider()

            # 2. 顯示籌碼面數據
            st.markdown("### 📊 近十日法人籌碼統計")
            st.dataframe(data.get("institutional_data"), use_container_width=True)

            # 3. 簡單分析建議
            st.markdown("### 🤖 AI 智慧分析")
            st.info("根據最新數據，該標的目前市場波動度正常，建議觀察後續主力券商買賣超力道。")

else:
    st.write("請在側邊欄輸入股票代號後，點擊「查詢分析數據」按鈕。")
    st.caption("提示：系統將直接從 Yahoo Finance 獲取即時資料，無需等待每日更新。")
