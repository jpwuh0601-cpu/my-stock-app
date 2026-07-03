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
                data = json.load(f)
                return data if isinstance(data, dict) else {}
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
    
    # 【最強防禦】：強制將任何型別轉換為 List of Dictionaries
    if raw is None:
        processed_data = []
    elif isinstance(raw, list):
        processed_data = raw
    elif isinstance(raw, dict):
        processed_data = [raw]
    else:
        processed_data = [{"數據": str(raw)}]
    
    # 執行表格顯示
    if processed_data:
        try:
            # 確保每一個元素都是字典
            clean_list = [item if isinstance(item, dict) else {"數據": str(item)} for item in processed_data]
            
            # 建立 DataFrame，強制指派 index
            df = pd.DataFrame(clean_list, index=[i for i in range(len(clean_list))])
            st.table(df)
        except Exception as e:
            st.error(f"表格格式解析失敗: {e}")
            st.write("原始資料:", raw)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
