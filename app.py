import streamlit as st
import json
import os
import pandas as pd

# 頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """安全讀取 JSON 數據"""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📊 AI 智能投資決策儀表板")
    
    # 載入數據
    data = load_data()
    
    # 提取數據 (防禦性編程：若無對應欄位，預設為 0 或空值)
    price = data.get("price", 0)
    bvps = data.get("bvps", 0)
    financials = data.get("financials", {}).get("2025Q1", {})
    eps = financials.get("EPS", 0)
    
    # 1. 核心指標區塊
    st.subheader("核心財務指標")
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(price):,.2f}")
    cols[1].metric("每股淨值 (BVPS)", f"{float(bvps):.2f}")
    cols[2].metric("最新 EPS", f"{float(eps):.2f}")
    cols[3].metric("融資券比", f"{data.get('margin_ratio', 0)}%")

    # 2. 籌碼與主力區塊
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("三大法人買賣超")
        df_inst = pd.DataFrame(data.get("institutional_investors", []))
        st.dataframe(df_inst, use_container_width=True, hide_index=True) if not df_inst.empty else st.write("無數據")
        
    with col2:
        st.subheader("主力券商買進")
        df_broker = pd.DataFrame(data.get("top_brokers", []))
        st.dataframe(df_broker, use_container_width=True, hide_index=True) if not df_broker.empty else st.write("無數據")

    # 3. AI 分析區塊
    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
