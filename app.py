import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 強制路徑指向根目錄
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
        st.error(f"資料格式讀取錯誤: {e}")
        return None

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    # 邊欄選股按鈕
    st.sidebar.header("選股功能區")
    if st.sidebar.button("執行全市場分析"):
        st.sidebar.info("分析中，請稍候...")

    data = load_data()
    if not data:
        st.warning("⚠️ 系統載入中，請確認市場資料檔已更新。")
        return

    # 指標顯示區
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[2].metric("預估營收", f"{float(data.get('est_revenue', 0)):,.0f}")
    cols[3].metric("預估 EPS", f"{float(data.get('est_eps', 0)):.2f}")
    cols[4].metric("預估股利", f"{float(data.get('est_dividend', 0)):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 穩定的表格顯示邏輯
    def safe_render_table(key, title):
        st.subheader(title)
        items = data.get(key, [])
        if isinstance(items, list) and len(items) > 0:
            df = pd.DataFrame(items)
            # 確保 DataFrame 不為空且擁有正確的 Column
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.write("無數據可用")
        else:
            st.write("無數據可用")

    safe_render_table("institutional_investors", "三大法人買賣超")
    safe_render_table("top_brokers", "主力券商買賣")

    st.subheader("AI 市場分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
