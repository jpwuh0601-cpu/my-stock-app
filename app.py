import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 使用絕對路徑，確保無論環境如何都能找到檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_market_data():
    if not os.path.exists(FILE_PATH):
        st.error(f"錯誤：找不到資料庫檔案 (路徑: {FILE_PATH})")
        st.write("請檢查 GitHub Actions 是否確實產生了 market_data.json 檔案。")
        return None
    
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON 檔案損毀或無法讀取: {e}")
        return None

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if data_cache is not None:
        if ticker in data_cache:
            d = data_cache[ticker]
            st.success(f"已從離線資料庫載入 {ticker}")
            st.metric("最新股價", f"{float(d.get('price', 0)):.2f}")
            
            st.subheader("法人籌碼分析")
            inst_data = d.get("institutional_data", [])
            if inst_data:
                st.table(pd.DataFrame(inst_data))
            else:
                st.write("目前無法人籌碼資料")
            
            st.subheader("AI 深度分析")
            st.info(d.get("ai_prediction", "暫無分析數據"))
        else:
            st.warning(f"資料庫中無此代號: {ticker}")
            st.write(f"目前資料庫中有的代號為: {', '.join(data_cache.keys())}")
else:
    st.info("請輸入代號後點擊查詢。")
