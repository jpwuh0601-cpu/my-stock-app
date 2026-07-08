import streamlit as st
import json
import os
import pandas as pd
from worker import fetch_stock_data

st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

def load_local_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 專業股市決策儀表板")
    
    # 1. 輸入代號
    ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.button("即時查詢"):
        # 先檢查本地 JSON
        local_data = load_local_data()
        
        if ticker_input in local_data:
            s = local_data[ticker_input]
            st.success("已載入本地分析數據")
        else:
            # 若本地無資料，直接即時呼叫 worker.py 的 fetch_stock_data
            with st.spinner(f"正在即時從網路擷取 {ticker_input} 資訊..."):
                realtime_data = fetch_stock_data(ticker_input)
                if "error" in realtime_data:
                    st.error(f"查詢失敗: {realtime_data['error']}")
                    return
                # 構建一個臨時的資料結構
                info = realtime_data.get("info", {})
                s = {
                    "price": realtime_data.get("price", 0),
                    "nav": info.get("bookValue", "N/A"),
                    "pe": info.get("trailingPE", "N/A"),
                    "eps": info.get("trailingEps", "N/A"),
                    "change": 0, "kd": "N/A", "macd": "N/A", "rsi": "N/A"
                }
                st.info("即時資料已載入 (未包含完整分析報告)")

        # 顯示資料 (後續顯示邏輯與原先一致)
        st.metric("即時股價", s.get('price', 0))
        # ... (其餘 10 大版面顯示邏輯)
        st.write("詳細籌碼面與AI分析需等待每日自動任務更新")

if __name__ == "__main__":
    main()
