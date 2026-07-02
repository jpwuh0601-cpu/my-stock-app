import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 讀取數據 (絕對路徑)
def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f), True
        except:
            return {}, False
    return {}, False

data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

# --- 選股操作區 ---
st.markdown("### 🔍 股票分析控制台")
# 將輸入框與按鈕放在同一行
col1, col2 = st.columns([4, 1])
with col1:
    stock_code = st.text_input("輸入股票代碼", value="2330", placeholder="例如: 2330")
with col2:
    st.write("##") # 調整按鈕垂直位置對齊
    if st.button("執行選股分析"):
        st.toast(f"正在載入 {stock_code} 分析數據...", icon="🚀")

if not loaded:
    st.error("❌ 尚未讀取數據，請確認 GitHub Actions 已執行更新。")
else:
    # 核心財務指標
    st.subheader("核心財務指標")
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("本益比 (PE)", f"{data.get('pe_ratio', 0):.2f}")
    cols[2].metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    cols[3].metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    cols[4].metric("預估股利", f"{data.get('est_dividend', 0):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 主力券商表格
    st.subheader("10日主力券商買賣明細")
    if "top_brokers" in data:
        df_brokers = pd.DataFrame(data["top_brokers"])
        st.dataframe(df_brokers, use_container_width=True)

    # 法人數據
    st.subheader("三大法人買賣超")
    if "institutional_investors" in data:
        st.dataframe(pd.DataFrame(data["institutional_investors"]), use_container_width=True)
