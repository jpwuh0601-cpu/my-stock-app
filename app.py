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
    
    # 【關鍵修復】：將數據強制轉化為 Pandas 絕對可讀的 List 結構
    # 我們確保每一個項目都是字典，如果不是，就把它封裝成字典
    processed_list = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                processed_list.append(item)
            else:
                processed_list.append({"內容": str(item)})
    elif isinstance(raw, dict):
        processed_list.append(raw)
    elif raw is not None:
        processed_list.append({"內容": str(raw)})

    # 表格顯示
    if processed_list:
        try:
            # 使用列表長度明確生成 index，解決 Scalar 值導致的 ValueError
            df = pd.DataFrame(processed_list, index=[i for i in range(len(processed_list))])
            st.table(df)
        except Exception as e:
            st.error(f"表格格式解析異常: {e}")
            st.write("原始資料:", raw)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
