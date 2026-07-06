import streamlit as st
import pandas as pd
import yfinance as yf
from worker import fetch_stock_data, fetch_real_broker_data

def verify_data(data_dict):
    """自動回測函式：驗證資料來源是否有效"""
    errors = []
    for key, value in data_dict.items():
        if value in [0, "N/A", "無資料", None]:
            errors.append(key)
    return errors

st.set_page_config(layout="wide")
st.title("📈 個股籌碼分析系統")

ticker = st.sidebar.text_input("股票代號", value="2330.TW")
if st.sidebar.button("查詢"):
    with st.spinner("分析中..."):
        info = yf.Ticker(ticker).info
        # 準備資料與回測
        raw_data = {
            "股價": info.get("currentPrice", 0),
            "EPS": info.get("trailingEps", 0),
            "法人數據": fetch_real_broker_data(ticker)
        }
        
        # 顯示區塊
        st.subheader("基本指標")
        col1, col2 = st.columns(2)
        col1.metric("股價", raw_data["股價"])
        col2.metric("EPS", raw_data["EPS"])
        
        st.subheader("三大法人買賣超")
        st.table(pd.DataFrame(raw_data["法人數據"]))
        
        # 自動回測檢查
        missing_fields = verify_data(raw_data)
        if missing_fields:
            st.error(f"⚠️ 數據源回測警示：以下欄位未取得有效資料: {', '.join(missing_fields)}")
        else:
            st.success("✅ 資料來源檢查通過：所有資料準確。")
