import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 強制尋找檔案的防錯邏輯
def get_file_path():
    possible_paths = ["market_data.json", os.path.join(os.getcwd(), "market_data.json")]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def load_market_data():
    file_path = get_file_path()
    if not file_path:
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if ticker in data_cache:
        d = data_cache[ticker]
        
        # 安全獲取價格，避免 NoneType
        price = d.get("price") or 0
        st.metric("最新股價", f"{float(price):.2f}")
        
        st.subheader("法人籌碼分析")
        # 確保 inst_data 是一個 list，如果不是，強制轉為空列表
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                st.table(pd.DataFrame(inst_data))
            except:
                st.write("表格資料格式無法解析")
        else:
            st.write("目前無法人籌碼資料")
            
        st.subheader("AI 深度分析")
        st.info(d.get("ai_prediction", "暫無分析數據"))
    else:
        st.warning(f"資料庫中無此代號: {ticker} (請確認該股票是否已在每日自動分析清單中)")
else:
    st.info("請輸入代號後點擊查詢。")
