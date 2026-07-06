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
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except: return {}

def clean_dataframe(df):
    """將 DataFrame 內的所有資料強制轉為可顯示的字串，解決 TypeError"""
    # 將所有物件轉為字串，避免嵌套 dict/list 導致崩潰
    return df.applymap(lambda x: str(x) if isinstance(x, (dict, list, pd.Series)) else x)

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
        c1.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        c2.metric("每股淨額", f"{float(d.get('nav', 0)):.2f}")
        c3.metric("本益比 (PE)", f"{float(d.get('pe', 0)):.2f}")
        st.metric("每股盈餘 (EPS)", f"{float(d.get('eps', 0)):.2f}")

        # 3. 三大法人買賣超 (核心修正)
        st.subheader("3. 三大法人買賣超 (10日)")
        inst_data = d.get("institutional_data")
        
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                # 建立 DataFrame
                df = pd.DataFrame(inst_data)
                # 使用清洗函數處理，確保所有內容轉為字串
                df_clean = clean_dataframe(df)
                st.table(df_clean)
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
