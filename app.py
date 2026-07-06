import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
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
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if ticker in data_cache:
        d = data_cache.get(ticker)
        
        # 關鍵修正：如果 d 為 None，顯示資料異常提示
        if d is None:
            st.warning(f"代號 {ticker} 在資料庫中存在，但數據內容為空 (None)。請檢查 GitHub Actions 執行結果。")
        else:
            # 安全獲取各項數據，防止任何 NoneType 錯誤
            price = d.get("price") or 0
            st.metric("最新股價", f"{float(price):.2f}")
            
            st.subheader("法人籌碼分析")
            inst_data = d.get("institutional_data")
            if isinstance(inst_data, list) and len(inst_data) > 0:
                st.table(pd.DataFrame(inst_data))
            else:
                st.write("目前無法人籌碼資料")
            
            st.subheader("AI 深度分析")
            st.info(d.get("ai_prediction") or "暫無分析數據")
    else:
        st.warning(f"資料庫中無此代號: {ticker}")
else:
    st.info("請輸入代號後點擊查詢。")
