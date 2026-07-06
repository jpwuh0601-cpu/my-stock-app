import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def find_data_file():
    """自動搜尋可能的檔案路徑"""
    # 嘗試多個路徑，確保一定找得到檔案
    possible_paths = [
        "market_data.json",                                # 當前目錄
        os.path.join(os.getcwd(), "market_data.json"),     # 工作目錄
        os.path.join(os.path.dirname(__file__), "market_data.json") # 檔案目錄
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def load_market_data():
    file_path = find_data_file()
    if not file_path:
        st.error("系統錯誤：找不到 market_data.json。")
        st.write("請確認 GitHub Actions 是否有成功建立檔案。")
        return {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"檔案讀取失敗: {e}")
        return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
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
else:
    st.info("請輸入代號後點擊查詢。")
