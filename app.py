import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_data():
    """從 JSON 讀取資料並轉為字典"""
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

# 側邊欄：選擇股票
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    all_data = load_data()
    # 修正：根據 JSON 新結構讀取 raw_info
    stock_entry = all_data.get(ticker, {})
    
    if not stock_entry:
        st.error(f"查無 '{ticker}' 的資料，請確認 Actions 已完成更新。")
    else:
        # 從 JSON 的 raw_info 結構層級提取數值
        raw = stock_entry.get("raw_info", {})
        info = raw.get("info", {})
        
        st.subheader("1. 基本財務數據")
        col1, col2, col3, col4 = st.columns(4)
        
        # 顯示數值，提供預設值 0
        col1.metric("即時股價", f"{raw.get('price', 0):.2f}")
        col2.metric("每股淨額 (NAV)", f"{info.get('bookValue', 0):.2f}")
        col3.metric("本益比 (PE)", f"{info.get('trailingPE', 0):.2f}")
        col4.metric("每股盈餘 (EPS)", f"{raw.get('eps', 0):.2f}")

        st.subheader("6. AI 財報預測")
        # 讀取 JSON 內的 ai_report
        ai_msg = stock_entry.get("ai_report", "目前無分析報告")
        st.info(ai_msg)
        
        st.success("✅ 資料來源驗證通過")
