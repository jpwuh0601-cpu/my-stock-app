import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 強制指向根目錄下的檔案
FILE_PATH = os.path.join(os.getcwd(), "market_data.json")

@st.cache_data(ttl=600)
def load_data():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    # --- 選股與互動區域 ---
    st.sidebar.header("🔍 選股分析面板")
    
    # 選擇器
    stock_options = ["2330 台積電", "2317 鴻海", "2454 聯發科"]
    selected_stock = st.sidebar.selectbox("請選擇關注標的", ["請選擇"] + stock_options)
    
    # --- 新增：選股確定按鈕 ---
    if st.sidebar.button("確定分析"):
        if selected_stock == "請選擇":
            st.sidebar.error("請先選擇一支股票！")
        else:
            st.sidebar.success(f"已選定：{selected_stock}")
            st.session_state['active_stock'] = selected_stock
    # ---------------------------

    data = load_data()
    if not data:
        st.warning("⚠️ 系統正在更新數據中，請稍候...")
        return

    # 檢查是否已進行選擇
    if 'active_stock' in st.session_state:
        st.subheader(f"正在顯示：{st.session_state['active_stock']} 的分析報告")
    
    # 核心財務指標顯示
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
            st.dataframe(df, use_container_width=True)
        else:
            st.write("目前無相關數據")

    safe_render_table("institutional_investors", "三大法人買賣超")
    safe_render_table("top_brokers", "主力券商買賣")

    st.subheader("AI 市場分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
