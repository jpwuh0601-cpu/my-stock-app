import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 側邊欄：輸入股票代號
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = load_data()
    d = data.get(ticker)
    
    if not d:
        st.error(f"查無 '{ticker}' 資料，請確認 Actions 已成功更新 JSON。")
    else:
        # 1. & 2. 財務數據 (每股淨額/本益比/EPS)
        st.subheader("1. & 2. 即時報價與財務數據")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("即時股價", d.get('price', '0'))
        c2.metric("每股淨額 (NAV)", d.get('nav', '0'))
        c3.metric("本益比 (PE)", d.get('pe', '0'))
        c4.metric("每股盈餘 (EPS)", d.get('eps', '0'))

        # 3. 每季報表
        st.subheader("3. 歷史每季報表")
        st.info(d.get("quarterly_report", "目前無季度報表資料"))

        # 4. 法人買賣超 (加入顏色渲染)
        st.subheader("4. 三大法人十日買賣超")
        inst_data = d.get("institutional_data", [])
        if inst_data:
            df = pd.DataFrame(inst_data)
            st.dataframe(df.style.map(lambda x: 'color: red' if float(x) > 0 else 'color: green', subset=['外資', '投信', '自營商']))
        else:
            st.warning("目前無法人籌碼資料")

        # 5. 資券比與主力券商
        st.subheader("5. 資券比與主力券商買賣超")
        st.write(d.get("margin_trading", "資券比資料庫連結中..."))

        # 8. 即時新聞
        st.subheader("8. 即時新聞")
        st.write(d.get("news", "無最新新聞"))

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.success(d.get("ai_prediction", "AI 分析中..."))

        # 7. 年度預估
        st.subheader("7. 年度營收、EPS 與股利預估")
        st.write("預估資料載入中...")
