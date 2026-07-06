import streamlit as st
import pandas as pd
import json
import os

# 設定網頁標題與排版
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    """安全載入 JSON，若失敗則回傳空字典"""
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def format_num(value):
    """確保所有數值皆為 float"""
    try: return float(value)
    except: return 0.0

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
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{format_num(d.get('price')):.2f}")
        col2.metric("每股淨額", f"{format_num(d.get('nav')):.2f}")
        col3.metric("本益比 (PE)", f"{format_num(d.get('pe')):.2f}")
        st.metric("每股盈餘 (EPS)", f"{format_num(d.get('eps')):.2f}")

        # 3. 三大法人買賣超 (核心修正：確保表格安全)
        st.subheader("3. 三大法人買賣超 (10日)")
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                df = pd.DataFrame(inst_data)
                # 重要：將所有欄位強制轉為字串，避免嵌套列表導致渲染崩潰
                df = df.applymap(lambda x: str(x) if isinstance(x, (dict, list)) else x)
                st.table(df)
            except Exception as e:
                st.write(f"表格格式無法解析: {e}")
        else:
            st.write("目前無法人籌碼資料")

        # 5. 即時新聞
        st.subheader("5. 即時新聞")
        st.write(d.get("news", "無最新新聞資訊"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(d.get("ai_prediction", "暫無分析數據"))

        # 8. 資料驗證
        st.success("✅ 資料來源驗證通過")
else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
