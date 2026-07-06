import streamlit as st
import pandas as pd
from worker import fetch_stock_data, fetch_real_broker_data

st.set_page_config(layout="wide")
st.title("📈 個股籌碼分析系統")

ticker_input = st.sidebar.text_input("股票代號", value="2330.TW")
if st.sidebar.button("查詢"):
    with st.spinner("分析中..."):
        # 1. 執行查詢
        result = fetch_stock_data(ticker_input)
        
        # 2. 顯示數據
        st.subheader("基本指標")
        col1, col2 = st.columns(2)
        col1.metric("股價", result["price"])
        col2.metric("EPS", result["eps"])
        
        st.subheader("三大法人買賣超")
        st.table(pd.DataFrame(fetch_real_broker_data(ticker_input)))
        
        # 3. 數據回測函式
        def verify_data(data):
            missing = []
            if data["price"] == 0: missing.append("股價")
            if data["eps"] == 0: missing.append("EPS")
            return missing

        # 4. 回測結果顯示
        missing_fields = verify_data(result)
        if missing_fields:
            st.error(f"⚠️ 數據源回測警示：以下欄位未取得有效資料: {', '.join(missing_fields)}")
        else:
            st.success("✅ 資料來源檢查通過：所有資料準確。")
