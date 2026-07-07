import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_data():
    """讀取市場數據"""
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取資料..."):
        all_data = load_data()
        
        # 顯示所有可用的 key，方便除錯
        st.sidebar.write("目前 JSON 內的股票:", list(all_data.keys()))
        
        data = all_data.get(ticker)
        
        if not data:
            st.error(f"查無 '{ticker}' 資料。請確認 market_data.json 內包含此代號。")
        else:
            # 顯示對齊後的數據
            col1, col2, col3, col4 = st.columns(4)
            # 這裡使用 .get(key, 0) 確保即使資料為空也不會報錯
            col1.metric("即時股價", f"{data.get('price', 0):.2f}")
            col2.metric("每股淨額 (NAV)", f"{data.get('nav', 0):.2f}")
            col3.metric("本益比 (PE)", f"{data.get('pe', 0):.2f}")
            col4.metric("每股盈餘 (EPS)", f"{data.get('eps', 0):.2f}")
            
            st.subheader("6. AI 財報預測")
            st.info(data.get("ai_prediction", "暫無分析數據"))
            
            st.subheader("3. 三大法人買賣超 (10日)")
            st.write(data.get("institutional_data", "無資料"))
