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
    
    # 顯示股價，提供預設值 0.0 防止崩潰
    price = data.get("price", 0.0)
    st.metric("即時股價", f"{float(price):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 獲取資料並進行最嚴格的型別檢查
    raw = data.get("institutional_investors")
    
    # 這裡確保 processed_data 永遠是一個列表
    if isinstance(raw, list):
        processed_data = raw
    elif isinstance(raw, dict):
        processed_data = [raw]
    else:
        processed_data = []

    # 表格顯示：如果列表為空，則顯示提示，不執行 DataFrame 轉換
    if processed_data:
        try:
            df = pd.DataFrame(processed_data)
            st.table(df)
        except Exception as e:
            st.error(f"表格繪製異常: {e}")
            st.write("原始數據:", processed_data)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
