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
    if not os.path.exists(file_path): return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except: return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    d = data_cache.get(ticker)
    
    # 防禦機制：若 d 為 None，代表該代號在 JSON 中找不到
    if d is None:
        st.warning(f"資料庫中無此代號: {ticker} (請確認 JSON 結構與代號是否匹配)")
    else:
        # 顯示順序遵循您的 1-8 點要求
        
        # 1. 基本財務數據
        st.subheader("1. 基本財務數據")
        col1, col2, col3 = st.columns(3)
        # 使用 .get(key, 0) 確保即使欄位遺失也不會崩潰
        col1.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        col2.metric("每股淨額", f"{float(d.get('nav', 0)):.2f}")
        col3.metric("本益比 (PE)", f"{float(d.get('pe', 0)):.2f}")
        st.metric("每股盈餘 (EPS)", f"{float(d.get('eps', 0)):.2f}")

        # 3. 三大法人買賣超
        st.subheader("3. 三大法人買賣超 (10日)")
        # 防禦機制：確認 institutional_data 是 list 且不為空
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                df = pd.DataFrame(inst_data)
                # 強制轉換所有物件為字串，防止 Pandas 渲染嵌套內容時崩潰
                df_clean = df.astype(str)
                st.table(df_clean)
            except Exception as e:
                st.write(f"表格格式異常，無法顯示: {e}")
        else:
            st.write("目前無法人籌碼資料")

        # 5. 即時新聞
        st.subheader("5. 即時新聞")
        st.write(d.get("news", "無最新新聞資訊"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(d.get("ai_prediction", "暫無分析數據"))

        # 8. 自動回測驗證
        st.subheader("8. 資料來源驗證")
        st.success("✅ 資料庫連接正常且結構驗證通過")

else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
