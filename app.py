import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 側邊欄輸入
st.sidebar.header("查詢設定")
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner(f"正在即時獲取 {ticker_input} 的數據..."):
        # 直接呼叫 worker.py 獲取即時資料
        data = fetch_stock_data(ticker_input)
        
        if "error" in data:
            st.error(data["error"])
        else:
            # 1. 即時股價與基本面
            st.markdown(f"### {ticker_input.upper()} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            
            price = data.get('price', 0)
            change = data.get('change', 0)
            
            col1.metric("即時股價", f"{price:.2f}", f"{change:.2f}")
            col2.metric("每股淨值 (NAV)", f"{data.get('nav', 0):.2f}")
            col3.metric("本益比 (PE)", f"{data.get('pe', 0):.2f}")
            col4.metric("每股盈餘 (EPS)", f"{data.get('eps', 0):.2f}")
            
            st.divider()

            # 2. 三大法人籌碼
            st.markdown("### 📊 近十日法人籌碼統計")
            df = data.get("institutional_data")
            if df is not None:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("暫無法人籌碼資料")

            # 3. AI 分析建議
            st.markdown("### 🤖 AI 智慧分析")
            st.info("系統已成功讀取即時數據。建議：請參考上方籌碼變化進行判斷。")

else:
    st.write("請在左側輸入股票代號後，點擊「查詢分析數據」。")
    st.caption("本系統直接對接即時市場數據，無需依賴每日更新的 JSON 檔。")
