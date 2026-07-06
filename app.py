import streamlit as st
from worker import fetch_stock_data, fetch_real_broker_data
import pandas as pd

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

# 側邊欄設計
st.sidebar.header("系統設定")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="1301.TW")

st.title("📈 個股籌碼分析系統")
st.write("請在左側輸入代號並點擊「查詢股價數據」，系統將為您分析籌碼與財報數據。")

if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在為您讀取 Yahoo Finance 資料..."):
        data = fetch_stock_data(ticker)
        
        # 錯誤處理機制
        if data.get("error"):
            st.error(f"系統提示: {data['error']}")
        else:
            # 顯示介面
            st.subheader("基本指標")
            col1, col2 = st.columns(2)
            col1.metric("股價", f"{data['price']:.2f}")
            col2.metric("EPS", f"{data['eps']:.2f}")
            
            st.subheader("三大法人買賣超")
            st.table(pd.DataFrame(fetch_real_broker_data(ticker)))
            
            st.success("✅ 資料讀取完成")
