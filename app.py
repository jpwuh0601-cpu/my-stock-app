import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 設定路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

@st.cache_data(ttl=600)
def load_data():
    """ 具備防禦性的資料讀取，避免 JSONDecodeError 導致崩潰 """
    if not os.path.exists(FILE_PATH):
        return None
    
    # 檢查檔案是否為空
    if os.path.getsize(FILE_PATH) == 0:
        return None
        
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        # 如果檔案損毀，回傳 None 讓介面顯示載入中提示
        return None

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    # --- 邊欄選股與互動 ---
    st.sidebar.header("🔍 選股分析面板")
    stock_options = ["2330 台積電", "2317 鴻海", "2454 聯發科"]
    selected_stock = st.sidebar.selectbox("請選擇關注標的", ["請選擇"] + stock_options)
    
    if st.sidebar.button("確定分析"):
        if selected_stock == "請選擇":
            st.sidebar.error("請先選擇一支股票！")
        else:
            st.session_state['active_stock'] = selected_stock
            st.sidebar.success(f"已切換至：{selected_stock}")

    # --- 載入數據 ---
    data = load_data()
    if data is None:
        st.info("⚠️ 數據同步中，請稍候... (若持續出現此訊息，請檢查分析任務是否成功執行)")
        return

    # 顯示指標
    if 'active_stock' in st.session_state:
        st.subheader(f"當前分析標的: {st.session_state['active_stock']}")
    
    cols = st.columns(6)
    # 使用 float() 強制轉型，避免型態衝突
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[2].metric("預估營收", f"{float(data.get('est_revenue', 0)):,.0f}")
    cols[3].metric("預估 EPS", f"{float(data.get('est_eps', 0)):.2f}")
    cols[4].metric("預估股利", f"{float(data.get('est_dividend', 0)):.2f}")
    cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")

    # 穩定的表格顯示
    def safe_render_table(key, title):
        st.subheader(title)
        items = data.get(key, [])
        if isinstance(items, list) and len(items) > 0:
            try:
                df = pd.DataFrame([dict(item) for item in items])
                st.dataframe(df, use_container_width=True)
            except Exception:
                st.write("數據格式解析錯誤")
        else:
            st.write("無數據可用")

    safe_render_table("institutional_investors", "三大法人買賣超")
    safe_render_table("top_brokers", "主力券商買賣")

    st.subheader("AI 市場分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
