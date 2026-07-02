import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    data = load_data()
    st.title("📈 AI 智能金融監控終端")
    
    # 顯示目前所有可用的鍵值 (除錯用)
    st.write("---")
    
    # 動態顯示所有資料
    for key, value in data.items():
        st.subheader(f"項目: {key}")
        
        if isinstance(value, list):
            try:
                df = pd.DataFrame(value)
                st.table(df)
            except:
                st.write(value)
        elif isinstance(value, dict):
            st.json(value)
        else:
            st.write(value)
            
    with st.expander("🔍 原始數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
