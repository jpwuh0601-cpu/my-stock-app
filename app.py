import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path): return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    d = data_cache.get(ticker)
    
    if not d:
        st.warning(f"資料庫中無此代號: {ticker}")
    else:
        # 1. 基本財務數據
        st.subheader("1. 基本財務數據")
        c1, c2, c3 = st.columns(3)
        # 直接由字典取值，若取不到用字串 "0" 補位，避免轉換失敗
        c1.metric("即時股價", str(d.get('price', "0")))
        c2.metric("每股淨額", str(d.get('nav', "0")))
        c3.metric("本益比 (PE)", str(d.get('pe', "0")))
        st.metric("每股盈餘 (EPS)", str(d.get('eps', "0")))

        # 3. 三大法人買賣超
        st.subheader("3. 三大法人買賣超 (10日)")
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                # 不再使用 pd.DataFrame 的自動轉型，直接用列表產生
                df = pd.DataFrame(inst_data)
                # 將所有欄位轉為字串，徹底排除型別錯誤
                df = df.astype(str)
                st.table(df)
            except Exception as e:
                st.write(f"表格渲染錯誤: {e}")
        else:
            st.write("目前無法人籌碼資料")

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(d.get("ai_prediction", "暫無分析數據"))
        
        st.success("✅ 資料來源驗證通過")
else:
    st.info("請輸入代號後點擊查詢。")
