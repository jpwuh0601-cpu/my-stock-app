import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

FILE_PATH = "market_data.json"

def load_data():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📊 AI 智能投資決策儀表板")
    data = load_data()
    
    # --- 1. 核心指標 ---
    price = data.get("price", 0)
    change = data.get("change", 0)
    bvps = data.get("bvps", 0)
    financials = data.get("financials", {}).get("2025Q1", {})
    eps = financials.get("EPS", 0)
    
    st.subheader("核心財務指標")
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(price):,.2f}", delta=f"{float(change):.2f}")
    cols[1].metric("每股淨值 (BVPS)", f"{float(bvps):.2f}")
    cols[2].metric("最新 EPS", f"{float(eps):.2f}")
    cols[3].metric("融資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")

    # --- 2. 互動式折線圖 ---
    st.subheader("近 30 日股價走勢")
    if "history" in data:
        df = pd.DataFrame({
            "日期": data["history"]["dates"],
            "收盤價": data["history"]["closes"]
        })
        fig = px.line(df, x="日期", y="收盤價", markers=True)
        fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("歷史數據載入中...")

    # --- 3. 籌碼與分析 ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("三大法人買賣超")
        df_inst = pd.DataFrame(data.get("institutional_investors", []))
        st.dataframe(df_inst, use_container_width=True, hide_index=True) if not df_inst.empty else st.write("無數據")
    
    with col2:
        st.subheader("主力券商買進")
        df_broker = pd.DataFrame(data.get("top_brokers", []))
        st.dataframe(df_broker, use_container_width=True, hide_index=True) if not df_broker.empty else st.write("無數據")

    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
