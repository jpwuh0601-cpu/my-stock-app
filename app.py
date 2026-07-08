import streamlit as st
import json
import os
import pandas as pd

# 設置頁面
st.set_page_config(page_title="股市系統", layout="centered")

def load_data():
    """ 安全載入 JSON，若失敗則回傳空字典 """
    if not os.path.exists("market_data.json"):
        return {"error": "檔案不存在"}
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"讀取失敗: {str(e)}"}

def main():
    st.title("📈 股市決策儀表板")
    
    # 載入資料
    data = load_data()
    
    if isinstance(data, dict) and "error" in data:
        st.error(data["error"])
        return

    # 簡單的搜尋 UI
    ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.button("確認查詢"):
        st.session_state.current_ticker = ticker_input

    target = st.session_state.get("current_ticker", ticker_input)

    if target in data:
        st.success(f"正在顯示: {target}")
        s = data[target]
        
        # 1. 即時股價 (漲紅跌綠)
        change = s.get('change', 0)
        color = "red" if change >= 0 else "green"
        st.markdown(f"### 即時股價: <span style='color:{color}'>{s.get('price', 'N/A')}</span>", unsafe_allow_html=True)
        
        # 2. 基本資訊
        cols = st.columns(3)
        cols[0].metric("每股淨值", s.get('nav', 0))
        cols[1].metric("本益比", s.get('pe', 0))
        cols[2].metric("EPS", s.get('eps', 0))
        
        st.write("---")
        st.write("資料已成功載入，更多詳細指標請參考後續頁面。")
    else:
        st.info("請輸入代號並點擊確認查詢。")

if __name__ == "__main__":
    main()
