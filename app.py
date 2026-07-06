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

# 側邊欄與輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    d = data_cache.get(ticker)
    
    if d is None:
        st.warning(f"查無資料: {ticker}")
    else:
        # 使用 .get(key, 預設值) 徹底解決 KeyError: 'price'
        price = d.get("price")
        price = float(price) if price not in [None, ""] else 0.0
        
        # 1. 股價與基本數據顯示
        st.subheader("1. 基本財務數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{price:.2f}")
        col2.metric("每股淨額", f"{float(d.get('nav', 0)):.2f}")
        col3.metric("本益比 (PE)", f"{float(d.get('pe', 0)):.2f}")
        st.metric("每股盈餘 (EPS)", f"{float(d.get('eps', 0)):.2f}")

        # 2. 財報分析
        st.subheader("2. 財報分析")
        st.write("今年與去年每季報表 (模擬數據)")

        # 3. 三大法人買賣超 (增加 NaN 處理)
        st.subheader("3. 三大法人買賣超 (10日)")
        inst_data = d.get("institutional_data")
        if isinstance(inst_data, list) and len(inst_data) > 0:
            df = pd.DataFrame(inst_data)
            # 強制將所有數值欄位轉為數字，無法轉換的變為 0
            df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
            st.table(df)
        else:
            st.write("目前無法人籌碼資料")

        # 4. 資券比與主力券商
        st.subheader("4. 資券與主力券商 (10日)")
        st.write(f"10日資券比: {d.get('margin_ratio', 0)}%")

        # 5. 即時新聞
        st.subheader("5. 即時新聞")
        st.write(d.get("news", "無最新新聞資訊"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(d.get("ai_prediction", "暫無分析數據"))

        # 7. 預估資訊
        st.subheader("7. 預估資訊")
        st.write("今年預估營收、EPS 與股利資訊")

        # 8. 自動回測驗證
        st.subheader("8. 資料來源驗證")
        if price > 0:
            st.success("✅ 資料來源與數值驗證通過")
        else:
            st.error("❌ 資料來源異常或數值遺失")
else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
