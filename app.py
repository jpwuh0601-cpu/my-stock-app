import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 強制指向根目錄下的檔案
FILE_PATH = os.path.join(os.getcwd(), "market_data.json")

def load_data():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f), True
        except Exception:
            return {}, False
    return {}, False

data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

# 股票輸入操作區
stock_code = st.text_input("輸入股票代碼", value="2330")
if st.button("執行選股分析"):
    st.write(f"正在載入 {stock_code} 的分析報告...")

if not loaded:
    st.error("系統讀取資料中，請稍候或檢查 GitHub Actions...")
else:
    # 核心財務指標
    st.subheader("核心財務指標")
    cols = st.columns(6)
    cols[0].metric("股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("本益比", f"{data.get('pe_ratio', 0):.2f}")
    cols[2].metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    cols[3].metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    cols[4].metric("股利", f"{data.get('est_dividend', 0):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 三大法人：加入空值檢測
    st.subheader("三大法人買賣超 (10日)")
    inst_data = data.get("institutional_investors", [])
    if inst_data and isinstance(inst_data, list) and len(inst_data) > 0:
        st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
    else:
        st.write("目前無法人買賣超數據")

    # 主力券商：加入空值檢測
    st.subheader("10日主力券商買賣")
    broker_data = data.get("top_brokers", [])
    if broker_data and isinstance(broker_data, list) and len(broker_data) > 0:
        st.dataframe(pd.DataFrame(broker_data), use_container_width=True)
    else:
        st.write("目前無主力券商數據")
