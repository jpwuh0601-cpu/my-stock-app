import streamlit as st
import pandas as pd
import json
import os
import sys

# 1. 強制檢查 Streamlit 是否正確載入
if 'metric' not in dir(st):
    st.error("系統錯誤：Streamlit 載入異常，請確認安裝版本是否包含 st.metric。")
    st.stop()

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

# 側邊欄
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if ticker in data_cache:
        d = data_cache.get(ticker) or {}
        
        # 使用更穩定的顯示方式
        st.subheader(f"代號: {ticker}")
        st.write(f"最新股價: {float(d.get('price', 0)):.2f}")
        
        st.subheader("法人籌碼分析")
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            st.table(pd.DataFrame(inst_data))
        else:
            st.write("目前無法人籌碼資料")
            
        st.subheader("AI 深度分析")
        st.info(d.get("ai_prediction", "暫無分析數據"))
    else:
        st.warning(f"查無資料: {ticker}")
