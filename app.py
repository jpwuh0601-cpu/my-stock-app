import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 顯示當前目錄，幫助除錯
st.sidebar.write(f"當前工作目錄: {os.getcwd()}")

def load_market_data():
    path = "market_data.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return None # 回傳 None 代表檔案真的找不到

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if data_cache is None:
        st.error("錯誤：找不到 market_data.json 檔案。請檢查 GitHub Actions 執行結果。")
    elif not data_cache:
        st.warning("檔案存在但內容為空 ({} )。")
    else:
        # 顯示目前資料庫內有的所有代號，讓您確認資料結構
        available_tickers = list(data_cache.keys())
        st.write(f"目前資料庫內包含: {available_tickers}")
        
        raw_ticker = st.sidebar.text_input("輸入代號", value="2330.TW")
        ticker = raw_ticker.strip().upper()
        if ticker.isdigit(): ticker = f"{ticker}.TW"
        
        if ticker in data_cache:
            d = data_cache[ticker]
            st.metric("股價", d.get("price", 0))
            st.subheader("法人籌碼")
            st.table(pd.DataFrame(d.get("institutional_data", [])))
            st.info(d.get("ai_prediction", "無分析"))
        else:
            st.warning(f"找不到代號: {ticker}")
