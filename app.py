import streamlit as st
import json
import os
from worker import fetch_stock_data, fetch_real_broker_data

st.set_page_config(page_title="個股即時查詢", layout="wide")

st.title("📈 個股即時分析系統")

# 側邊欄：手動輸入代號並直接查詢
with st.sidebar.form("ticker_input_form"):
    user_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
    query_button = st.form_submit_button("立即查詢")

if query_button:
    with st.spinner(f"正在查詢 {user_ticker}，請稍候..."):
        try:
            # 直接在網頁端呼叫 worker.py 中的函數
            stock_info = fetch_stock_data(user_ticker)
            broker_info = fetch_real_broker_data(user_ticker)
            
            # 將結果直接顯示，不透過 GitHub Action 中轉
            st.subheader(f"分析結果: {user_ticker}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("當前股價", stock_info.get("price", "無資料"))
            with col2:
                st.metric("市場價值", stock_info.get("marketCap", "無資料"))
            
            st.write("### 券商分點明細")
            st.table(broker_info)
            
            # 同步更新本地 JSON 備份
            data = {user_ticker: {"price": stock_info.get("price"), "raw_info": stock_info}}
            with open("market_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            st.error(f"查詢失敗: {e}")
else:
    # 預設顯示上次的結果
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            st.json(data)
