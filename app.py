import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

@st.cache_data(ttl=600)
def load_data():
    if not os.path.exists(FILE_PATH):
        return None
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    # --- 新增：選股與互動區域 ---
    st.sidebar.header("選股功能區")
    if st.sidebar.button("執行全市場分析"):
        st.sidebar.info("正在啟動 AI 篩選流程...")
        # 這裡可以連結您的 main_task.py 或其他分析模組
    
    selected_stock = st.sidebar.selectbox("選擇關注標的", ["請選擇", "2330 台積電", "2317 鴻海", "2454 聯發科"])
    if selected_stock != "請選擇":
        st.sidebar.write(f"您已選擇: {selected_stock}")
    # ---------------------------

    data = load_data()
    if data is None or "error" in data:
        st.warning("⚠️ 系統載入中...")
        return

    # 指標區
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[2].metric("預估營收", f"{float(data.get('est_revenue', 0)):,.0f}")
    cols[3].metric("預估 EPS", f"{float(data.get('est_eps', 0)):.2f}")
    cols[4].metric("預估股利", f"{float(data.get('est_dividend', 0)):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 表格區
    st.subheader("三大法人買賣超")
    st.dataframe(pd.DataFrame(data.get("institutional_investors", [])), use_container_width=True)

    st.subheader("主力券商買賣")
    st.dataframe(pd.DataFrame(data.get("top_brokers", [])), use_container_width=True)

    st.subheader("AI 市場分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
