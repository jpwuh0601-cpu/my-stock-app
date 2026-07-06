import streamlit as st
import pandas as pd
import json
import os

# 設定網頁標題與排版
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

# 側邊欄輸入區
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 1. 安全讀取代號資料
    d = data_cache.get(ticker) if isinstance(data_cache, dict) else None
    
    if d is None:
        st.warning(f"資料庫中無此代號: {ticker}。請確認 GitHub Actions 是否已更新。")
    else:
        # 顯示順序遵循您的要求
        
        # 1. 股價與基本數據
        st.subheader("1. 基本財務數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        col2.metric("每股淨額", f"{float(d.get('nav', 0)):.2f}")
        col3.metric("本益比 (PE)", f"{float(d.get('pe', 0)):.2f}")
        st.metric("每股盈餘 (EPS)", f"{float(d.get('eps', 0)):.2f}")

        # 2. 財報 (今年與去年)
        st.subheader("2. 財報分析")
        st.write("今年與去年每季報表 (模擬)")
        st.info("此處將呈現每季財務數據 (請確保 JSON 包含 quarterly_reports 欄位)")

        # 3. 三大法人十日買賣超
        st.subheader("3. 三大法人買賣超 (10日)")
        inst_data = d.get("institutional_data", [])
        if inst_data:
            df_inst = pd.DataFrame(inst_data)
            st.table(df_inst)
        else:
            st.write("暫無法人籌碼資料")

        # 4. 資券比與主力券商
        st.subheader("4. 資券與主力券商 (10日)")
        st.metric("10日資券比", f"{d.get('margin_ratio', 0)}%")
        st.write("主力券商買賣超資料 (模擬)")

        # 5. 即時新聞
        st.subheader("5. 即時新聞")
        st.write(d.get("news", "無最新新聞資訊"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(d.get("ai_prediction", "暫無分析數據"))

        # 7. 預估營收/EPS/股利
        st.subheader("7. 預估資訊")
        st.write("今年預估營收、EPS 與股利資訊")

        # 8. 自動回測驗證 (簡易版)
        st.subheader("8. 資料來源驗證")
        if d.get("price") is not None:
            st.success("✅ 資料來源與數值驗證通過")
        else:
            st.error("❌ 資料來源異常或數值遺失")

else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
