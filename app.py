import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if not os.path.exists(file_path):
        st.error(f"找不到資料庫檔案: {file_path}")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON 解析失敗: {e}")
        return None

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

# 自動修正格式：如果是 2330 這種格式，自動補上 .TW
ticker = raw_ticker.strip()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在從離線資料庫載入..."):
        data_cache = load_market_data()
        
        if data_cache is not None:
            if ticker in data_cache:
                d = data_cache[ticker]
                st.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
                
                st.subheader("法人籌碼分析")
                inst_df = pd.DataFrame(d.get("institutional_data", []))
                if not inst_df.empty:
                    st.table(inst_df)
                else:
                    st.write("目前無法人籌碼資料")
                
                st.subheader("AI 深度分析")
                st.info(d.get("ai_prediction", "分析處理中..."))
            else:
                st.warning(f"資料庫中找不到代號: {ticker}。")
                st.write(f"目前資料庫內有的代號為: {', '.join(data_cache.keys())}")
else:
    st.info("請輸入代號並點擊查詢。")
