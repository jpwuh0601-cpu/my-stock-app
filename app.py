import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 確保讀取路徑準確
file_path = os.path.join(os.getcwd(), "market_data.json")

def load_data():
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f), True
        except:
            return {}, False
    return {}, False

data, loaded = load_data()

st.title("📊 AI 智能投資決策儀表板")

if not loaded:
    st.error("❌ 系統讀取數據失敗，請確認 GitHub Actions 自動化任務是否已執行。")
else:
    # 核心財務指標 (防錯處理：使用 .get(key, 0) 確保不會出現 TypeError)
    st.subheader("核心財務指標")
    
    # 建立一個安全的顯示格式函式
    def safe_format(val, fmt="{:,.2f}"):
        try:
            return fmt.format(float(val))
        except:
            return "0.00"

    cols = st.columns(6)
    cols[0].metric("股價", safe_format(data.get("price", 0)))
    cols[1].metric("本益比", safe_format(data.get("pe_ratio", 0)))
    cols[2].metric("預估營收", safe_format(data.get("est_revenue", 0), "{:,.0f}"))
    cols[3].metric("預估 EPS", safe_format(data.get("est_eps", 0)))
    cols[4].metric("預估股利", safe_format(data.get("est_dividend", 0)))
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}")

    # 三大法人買賣超
    st.subheader("三大法人買賣超 (10日)")
    if "institutional_investors" in data:
        df_inst = pd.DataFrame(data["institutional_investors"])
        st.dataframe(df_inst, use_container_width=True)

    # 主力券商買賣
    st.subheader("主力券商買賣")
    if "top_brokers" in data:
        st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)

    # 新聞動態
    st.subheader("市場動態")
    for news in data.get("news", []):
        st.write(f"• {news}")
