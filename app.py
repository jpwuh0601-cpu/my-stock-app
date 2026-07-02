import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("資料載入中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 【強制修正】：處理籌碼數據
    st.subheader("三大法人與籌碼數據")
    raw_data = data.get("institutional_investors")

    # 1. 檢查是否為字串 (JSON 格式的字串)
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except:
            raw_data = []

    # 2. 檢查是否為 None
    if raw_data is None:
        raw_data = []

    # 3. 確保最後轉為 DataFrame 的是 List 結構
    try:
        if isinstance(raw_data, list) and len(raw_data) > 0:
            df = pd.DataFrame(raw_data)
            st.dataframe(df, use_container_width=True)
        elif isinstance(raw_data, dict):
            df = pd.DataFrame([raw_data])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error(f"數據顯示失敗: {e}")
        st.write("原始類型:", type(raw_data))

    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無數據"))

if __name__ == "__main__":
    main()
