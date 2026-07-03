import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    # 強制指向當前目錄下的檔案，避免路徑錯誤
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    raw = data.get("institutional_investors")
    
    # 【最終硬編碼解析】：強制重塑資料結構
    processed_list = []
    if isinstance(raw, list):
        processed_list = raw
    elif isinstance(raw, dict):
        processed_list = [raw]
    
    if processed_list:
        try:
            # 使用 pd.DataFrame 並強制指定 list 的長度作為 index
            df = pd.DataFrame(processed_list, index=[i for i in range(len(processed_list))])
            st.table(df)
        except Exception as e:
            st.error(f"表格格式解析失敗: {e}")
            st.write("原始資料結構:", raw)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據結構"):
        st.json(data)

if __name__ == "__main__":
    main()
