import streamlit as st
import json
import os

# 診斷：設定頁面配置並確保錯誤能顯示在螢幕上
st.set_page_config(page_title="股市系統", layout="centered")

def main():
    st.title("📈 股市決策儀表板")
    
    # Debug: 檢查檔案是否存在
    data_file = "market_data.json"
    if not os.path.exists(data_file):
        st.error(f"錯誤: {data_file} 找不到。請確保該檔案在專案根目錄。")
        return

    # Debug: 嘗試載入資料
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        st.error(f"JSON 解析錯誤: {e}")
        return

    # 介面顯示
    ticker_input = st.text_input("輸入股票代號", "2330.TW")
    if st.button("查詢股價"):
        if ticker_input in data:
            st.session_state.current_ticker = ticker_input
        else:
            st.warning(f"找不到代號: {ticker_input}")

    # 顯示內容
    ticker = st.session_state.get("current_ticker", ticker_input)
    if ticker in data:
        st.success(f"已載入 {ticker}")
        s = data[ticker]
        st.metric("即時股價", s.get('price', 0), delta=s.get('change', 0))
    else:
        st.info("請輸入代號並點擊查詢。")

if __name__ == "__main__":
    main()
