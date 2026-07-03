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
    
    # 顯示股價
    price = data.get("price", 0)
    st.metric("即時股價", f"{float(price):,.2f}")
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    raw = data.get("institutional_investors")
    
    # 1. 強制重塑為字典列表，這是最穩定結構
    clean_list = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                clean_list.append(item)
            else:
                clean_list.append({"內容": str(item)})
    elif isinstance(raw, dict):
        clean_list.append(raw)
    elif raw is not None:
        clean_list.append({"內容": str(raw)})

    # 2. 如果資料有內容，使用明確的 Index 進行 DataFrame 建立
    if clean_list:
        try:
            # 確保所有字典的 keys 一致，如果沒有則補上，這是 DataFrame 最喜歡的格式
            df = pd.DataFrame(clean_list, index=range(len(clean_list)))
            st.table(df)
        except Exception as e:
            st.error(f"表格格式解析失敗: {e}")
            st.write("原始數據:", raw)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
