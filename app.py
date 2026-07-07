import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_data():
    """從 JSON 讀取資料"""
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        all_data = load_data()
        data = all_data.get(ticker)
        
        if not data:
            st.error(f"查無 '{ticker}' 資料。請確認 GitHub Actions 已成功執行並產生 JSON。")
        else:
            # 顯示對齊後的平鋪數據
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data.get('price', 0):.2f}")
            col2.metric("每股淨額 (NAV)", f"{data.get('nav', 0):.2f}")
            col3.metric("本益比 (PE)", f"{data.get('pe', 0):.2f}")
            col4.metric("每股盈餘 (EPS)", f"{data.get('eps', 0):.2f}")
            
            st.subheader("6. AI 財報預測")
            st.info(data.get("ai_report", "暫無 AI 分析數據"))
            
            # 若您需要顯示法人數據
            st.subheader("3. 三大法人買賣超 (10日)")
            st.write(data.get("institutional_data", "無資料"))
