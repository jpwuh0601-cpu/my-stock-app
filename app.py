import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 設定路徑：永遠指向當前目錄下的檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

@st.cache_data(ttl=60)
def load_data():
    """帶有完整錯誤處理的資料載入函式"""
    if not os.path.exists(FILE_PATH):
        return None
    
    # 若檔案為空 (0 bytes) 直接回傳 None
    if os.path.getsize(FILE_PATH) == 0:
        return None
        
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        # 如果格式錯誤 (例如寫入中)，回傳 None 讓前端顯示提示
        return None

def safe_render_table(data, key, title):
    """安全渲染表格的輔助函式"""
    st.subheader(title)
    items = data.get(key, [])
    
    if isinstance(items, list) and len(items) > 0:
        # 強制轉換為 Python 字典清單，避開 Pandas Numpy 解析錯誤
        try:
            df = pd.DataFrame([dict(i) for i in items])
            st.dataframe(df, use_container_width=True)
        except Exception:
            st.write("表格資料格式無法解析")
    else:
        st.write("無即時數據")

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    # 載入資料
    data = load_data()
    
    if data is None:
        st.info("⚠️ 數據同步中，請稍候片刻...")
        return

    # 1. 核心財務指標
    st.subheader("核心財務指標")
    cols = st.columns(6)
    cols[0].metric("最新股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("本益比", f"{float(data.get('pe_ratio', 0)):.1f}")
    cols[2].metric("淨值", f"{float(data.get('bvps', 0)):.1f}")
    cols[3].metric("融資券比", f"{data.get('margin_ratio', 0)}%")
    cols[4].metric("營收預估", f"{float(data.get('est_revenue', 0)):,.0f}")
    cols[5].metric("EPS 預估", f"{float(data.get('est_eps', 0)):.2f}")

    # 2. 表格區塊
    safe_render_table(data, "institutional_investors", "三大法人買賣超")
    safe_render_table(data, "top_brokers", "主力券商買賣")

    # 3. AI 分析區塊
    st.subheader("AI 市場趨勢分析")
    st.success(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
