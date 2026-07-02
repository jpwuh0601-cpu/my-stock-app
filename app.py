import streamlit as st
import json
import os
import pandas as pd

# 頁面配置 (必須位於最上方)
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 確保在 Streamlit Cloud 環境下的路徑正確
# 使用絕對路徑以避免當前工作目錄變更導致的問題
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

@st.cache_data(ttl=600) # 快取資料 10 分鐘，避免頻繁讀取造成的 IO 阻塞
def load_data():
    """安全載入 JSON 資料的函式"""
    if not os.path.exists(FILE_PATH):
        return None
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    data = load_data()

    if data is None:
        st.warning("⚠️ 系統載入中：尚未偵測到市場數據檔案，請稍後...")
        return
    
    if "error" in data:
        st.error(f"資料讀取失敗: {data['error']}")
        return

    # 顯示指標區
    try:
        cols = st.columns(6)
        cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
        cols[1].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
        cols[2].metric("預估營收", f"{float(data.get('est_revenue', 0)):,.0f}")
        cols[3].metric("預估 EPS", f"{float(data.get('est_eps', 0)):.2f}")
        cols[4].metric("預估股利", f"{float(data.get('est_dividend', 0)):.2f}")
        cols[5].metric("10日資券比", f"{data.get('margin_ratio', 0)}%")
    except (ValueError, TypeError):
        st.error("資料格式轉換錯誤，請檢查 market_data.json 內容")

    # 顯示表格區
    st.subheader("三大法人買賣超")
    if "institutional_investors" in data:
        st.dataframe(pd.DataFrame(data["institutional_investors"]), use_container_width=True)

    st.subheader("主力券商買賣")
    if "top_brokers" in data:
        st.dataframe(pd.DataFrame(data["top_brokers"]), use_container_width=True)

    st.subheader("AI 市場分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
