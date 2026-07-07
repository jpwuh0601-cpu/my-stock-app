import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = load_data()
    # 修正：直接讀取該 ticker 的內容
    stock_data = data.get(ticker, {})
    
    if not stock_data:
        st.error(f"查無 '{ticker}' 資料")
    else:
        # 從 raw_info 內撈取數據
        raw = stock_data.get("raw_info", {})
        info = raw.get("info", {})
        
        st.subheader("1. 基本財務數據")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("即時股價", f"{raw.get('price', 0):.2f}")
        c2.metric("每股淨額 (NAV)", f"{info.get('bookValue', 0):.2f}")
        c3.metric("本益比 (PE)", f"{info.get('trailingPE', 0):.2f}")
        c4.metric("每股盈餘 (EPS)", f"{raw.get('eps', 0):.2f}")

        st.subheader("3. 三大法人買賣超 (10日)")
        st.write("資料處理中...") # 後續再補齊表格渲染
        
        st.subheader("6. AI 財報預測")
        st.info(stock_data.get("ai_report", "暫無分析數據"))
