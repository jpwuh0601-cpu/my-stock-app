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
    
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    raw = data.get("institutional_investors")
    
    try:
        # 強制邏輯：確保 data_list 是一個列表
        if raw is None:
            data_list = []
        elif isinstance(raw, list):
            data_list = raw
        else:
            # 如果 raw 是字典，把它放入列表中
            data_list = [raw]
            
        # 表格顯示
        if data_list:
            # 關鍵修正：給 DataFrame 指定 Index，這是解決 Scalar ValueError 的唯一解
            df = pd.DataFrame(data_list, index=range(len(data_list)))
            st.table(df)
        else:
            st.info("目前無籌碼數據。")
            
    except Exception as e:
        st.error(f"表格格式解析失敗: {e}")
        st.write("原始數據結構:", raw)

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
