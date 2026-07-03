import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    raw = data.get("institutional_investors")
    
    # 【終極防禦】：無論來源是什麼，強制將其重塑為 List of Dicts
    processed_list = []
    if isinstance(raw, list):
        processed_list = raw
    elif isinstance(raw, dict):
        processed_list = [raw]
    
    # 執行繪圖
    if processed_list:
        try:
            # 強制將資料中的值轉為字串，徹底避免數值型別衝突
            sanitized_data = [{str(k): str(v) for k, v in item.items()} for item in processed_list]
            
            # 使用列表長度明確指定 Index
            df = pd.DataFrame(sanitized_data, index=range(len(sanitized_data)))
            st.table(df)
        except Exception as e:
            st.error(f"表格格式解析失敗: {e}")
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
