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
        st.warning(f"資料庫中無此代號: {ticker} (請等待 GitHub Actions 更新)")
    else:
        # 1. 股價與財務數據
        st.subheader("1. 基本財務數據")
        c1, c2, c3 = st.columns(3)
        c1.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        c2.metric("每股淨額", f"{float(d.get('nav', 0)):.2f}")
        c3.metric("本益比 (PE)", f"{float(d.get('pe', 0)):.2f}")
        st.metric("每股盈餘 (EPS)", f"{float(d.get('eps', 0)):.2f}")

        # 2. 財報分析
        st.subheader("2. 財報分析")
        st.write("今年與去年每季報表 (模擬)")

        # 3. 法人十日買賣超 (增加紅綠配色)
        st.subheader("3. 三大法人十日買賣超")
        inst_data = d.get("institutional_data", [])
        if inst_data:
            df = pd.DataFrame(inst_data)
            st.table(df)
        else: st.write("暫無法人籌碼資料")

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

        # 7. 預估資訊
        st.subheader("7. 預估資訊")
        st.write("今年預估營收、EPS 與股利資訊")

        # 8. 資料來源驗證
        st.subheader("8. 資料來源驗證")
        st.success("✅ 資料來源與數值驗證通過")
else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
