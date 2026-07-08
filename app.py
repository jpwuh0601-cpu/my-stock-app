import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

def load_market_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取檔案失敗: {e}")
            return None
    return None

ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在解析市場數據..."):
        data = load_market_data()
        
        # 防禦邏輯：確保 data 不為空，且包含該代號
        if data is None:
            st.error("⚠️ 無法讀取數據檔 market_data.json")
        elif ticker_input not in data:
            st.error(f"⚠️ 數據檔中找不到代號 {ticker_input}，請確認自動化任務是否已執行")
        else:
            stock_info = data[ticker_input]
            
            # 確保 stock_info 不為 None
            if not isinstance(stock_info, dict):
                st.error("⚠️ 資料格式異常")
            else:
                # 顯示數據
                st.markdown(f"### {ticker_input} 即時分析")
                price = stock_info.get('price', 0)
                change = stock_info.get('change', 0)
                
                col1, col2 = st.columns(2)
                col1.metric("即時股價", f"{price}")
                col2.metric("今日漲跌", f"{change}")
                
                st.success("數據載入成功！")
