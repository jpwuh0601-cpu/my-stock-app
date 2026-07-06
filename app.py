import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    """從 JSON 離線資料庫載入分析結果"""
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取離線資料庫..."):
        data_cache = load_market_data()
        
        # 強制讀取 JSON，完全繞過 Yahoo API
        if ticker in data_cache:
            d = data_cache[ticker]
            st.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
            
            st.subheader("法人籌碼分析")
            st.table(pd.DataFrame(d.get("institutional_data", [])))
            
            st.subheader("AI 深度分析")
            st.info(d.get("ai_prediction", "分析處理中..."))
        else:
            st.warning("系統提示：目前尚未分析此代號，請確認 GitHub Actions 是否已執行更新。")
else:
    st.info("請輸入代號並點擊查詢，系統將直接讀取由 GitHub 自動更新的離線數據庫。")
