import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if ticker in data_cache:
        d = data_cache.get(ticker) or {}
        
        # 1. 確保價格顯示正常
        price = d.get("price") or 0
        st.metric("最新股價", f"{float(price):.2f}")
        
        # 2. 安全讀取法人資料，若找不到該欄位，自動補上空列表
        st.subheader("法人籌碼分析")
        inst_data = d.get("institutional_data")
        
        if inst_data and isinstance(inst_data, list):
            try:
                st.table(pd.DataFrame(inst_data))
            except:
                st.write("資料格式無法轉為表格")
        else:
            st.write("目前無法人籌碼資料")
            
        # 3. 安全讀取 AI 分析
        st.subheader("AI 深度分析")
        st.info(d.get("ai_prediction") or "暫無分析數據")
    else:
        st.warning(f"資料庫中無此代號: {ticker}")
else:
    st.info("請輸入代號後點擊查詢。")
