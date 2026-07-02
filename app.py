import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 確保讀取路徑準確
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

if not loaded:
    st.error("❌ 系統讀取數據失敗，請等待每日自動排程更新。")
else:
    # 核心財務指標 (修正 UI 渲染語法)
    st.subheader("核心財務指標")
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):,.2f}")
    cols[2].metric("預估營收", f"{data.get('est_revenue', 0):,.0f}")
    cols[3].metric("預估 EPS", f"{data.get('est_eps', 0):.2f}")
    
    # 修正：移除過時的 use_container_width，改用新版語法
    st.subheader("三大法人買賣超 (10日)")
    if "institutional_investors" in data:
        df_inst = pd.DataFrame(data["institutional_investors"])
        # 改用 width=None 確保相容性
        st.dataframe(df_inst, use_container_width=True) 
    
    st.subheader("主力券商買賣")
    if "top_brokers" in data:
        st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)

st.divider()
st.info("若畫面持續轉圈，請檢查 GitHub Action 的 'main' 分支是否已成功執行 'chore: update market data'。")
