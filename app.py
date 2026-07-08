import streamlit as st
import json
import pandas as pd
import os

# 診斷：確保頁面配置最優先
st.set_page_config(page_title="股市決策系統", layout="centered")

def debug_log(msg):
    # 協助您在右側 Console 查看進度
    print(f"[DEBUG] {msg}")

def load_data():
    debug_log("開始讀取資料...")
    if not os.path.exists("market_data.json"):
        debug_log("錯誤: market_data.json 不存在")
        return {}
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            debug_log(f"讀取成功，共 {len(data)} 筆數據")
            return data
    except Exception as e:
        debug_log(f"JSON 解析錯誤: {e}")
        return {}

def main():
    debug_log("進入主程式")
    st.title("📈 股市決策儀表板")
    
    data = load_data()
    
    # 簡單的查詢區塊
    ticker_input = st.text_input("輸入股票代號", "2330.TW")
    
    if st.button("查詢"):
        st.session_state.current_ticker = ticker_input
        st.rerun() # 強制重整以刷新顯示

    ticker = st.session_state.get("current_ticker", ticker_input)
    
    if ticker in data:
        st.success(f"已載入 {ticker} 資料")
        s = data[ticker]
        
        # 顯示即時股價
        st.metric("即時股價", s.get('price', 0), delta=s.get('change', 0))
        
        # 顯示其他資訊
        st.write("詳細資訊:", s)
    else:
        st.info("請輸入代號並點擊查詢，或等待系統資料更新。")

if __name__ == "__main__":
    debug_log("啟動程式...")
    main()
