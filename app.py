import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data

# 頁面配置
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 優先讀取 GitHub Action 產生的資料
def load_market_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取數據庫..."):
        data_cache = load_market_data()
        
        # 邏輯：優先讀取已分析過的本地 JSON，若無則嘗試呼叫 worker 抓取 (需注意頻率)
        if ticker in data_cache:
            d = data_cache[ticker]
            st.success("已載入最新分析數據")
            
            # 1. 股價與財務數據
            st.subheader("1. 股價與財務數據")
            cols = st.columns(3)
            cols[0].metric("即時股價", f"{d.get('price', 0):.2f}")
            cols[1].metric("EPS", f"{d.get('eps', 0):.2f}")
            
            # 2. 法人籌碼視覺化
            st.subheader("2. 法人籌碼統計")
            inst_data = d.get("institutional_data", [])
            if inst_data:
                inst_df = pd.DataFrame(inst_data)
                st.dataframe(inst_df, use_container_width=True)
            else:
                st.warning("無近期法人籌碼數據。")
            
            # 3. AI 深度分析
            st.subheader("6. AI 財報預測")
            st.info(d.get("ai_prediction", "分析處理中..."))
            
        else:
            st.warning("系統尚未完成該股票分析，請等待 GitHub Action 自動執行任務。")
            st.info("您可至 Actions 面板手動觸發 `Daily Stock Analysis` 工作流。")

else:
    st.info("請輸入代號並點擊查詢，系統將優先讀取已分析過的資料庫，不會觸發 API 限制。")
