import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 確保路徑正確
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    if not os.path.exists(FILE_PATH):
        return None
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def main():
    st.title("📊 AI 智能投資決策儀表板")
    data = load_data()

    if data is None:
        st.info("⚠️ 數據加載中...")
        return

    # 顯示指標 (使用 float 強制轉型，避免型態衝突)
    cols = st.columns(6)
    cols[0].metric("股價", f"{float(data.get('price', 0)):,.2f}")
    
    # 針對表格渲染的修正邏輯
    st.subheader("三大法人買賣超")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list) and len(inst_data) > 0:
        # 關鍵修正：將 dict 轉換為 DataFrame 前，先進行簡單的格式重塑，避開 numpy 錯誤
        df_inst = pd.DataFrame([dict(item) for item in inst_data])
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.write("無數據")

    st.subheader("主力券商買賣")
    broker_data = data.get("top_brokers", [])
    if isinstance(broker_data, list) and len(broker_data) > 0:
        df_broker = pd.DataFrame([dict(item) for item in broker_data])
        st.dataframe(df_broker, use_container_width=True)

if __name__ == "__main__":
    main()
