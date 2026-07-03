import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 1. 取得原始資料
    raw = data.get("institutional_investors")
    
    # 2. 絕對防禦處理：確保結構為 List of Dictionaries
    processed_list = []
    if isinstance(raw, list):
        processed_list = raw
    elif isinstance(raw, dict):
        processed_list = [raw]
    
    # 3. 如果資料庫中有資料，進行表格轉換
    if processed_list:
        try:
            # 強制指派 index 徹底解決 scalar values 報錯
            df = pd.DataFrame(processed_list, index=range(len(processed_list)))
            st.table(df)
        except Exception as e:
            st.error(f"表格繪製錯誤: {e}")
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
