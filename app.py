import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    """強制從專案根目錄讀取 GitHub Actions 產出的離線數據"""
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"資料讀取錯誤: {e}")
            return {}
    return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 檢查 data_cache 是否為空或資料庫中是否有該 ticker
    if data_cache and ticker in data_cache:
        d = data_cache[ticker]
        
        # 使用 .get() 並加上預設值，防止 AttributeError
        price = d.get("price", 0)
        institutional_data = d.get("institutional_data", [])
        ai_prediction = d.get("ai_prediction", "暫無分析數據")
        
        st.success(f"已從離線資料庫載入 {ticker}")
        st.metric("最新股價", f"{float(price):.2f}")
        
        st.subheader("法人籌碼分析")
        if institutional_data:
            st.table(pd.DataFrame(institutional_data))
        else:
            st.write("目前無法人籌碼資料")
        
        st.subheader("AI 深度分析")
        st.info(ai_prediction)
    
    elif not data_cache:
        st.error("系統錯誤：無法讀取到有效的資料庫檔案 (market_data.json)。")
        st.write("建議檢查 GitHub Actions 是否執行成功。")
    else:
        st.warning(f"資料庫中無此代號: {ticker}")
        st.write("提示：若要分析此股票，請將其加入 `tickers.txt` 並等待 GitHub Actions 自動更新。")
else:
    st.info("請輸入代號後點擊查詢 (僅限資料庫中已有的股票)。")
