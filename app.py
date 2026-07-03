import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據，確保回傳非空的字典"""
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
    
    # 核心指標：處理 None 值防護
    price = data.get("price") or 0.0
    st.metric("即時股價", f"{float(price):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 【關鍵防禦】：強制處理 raw 為空值或 None 的情況
    raw = data.get("institutional_investors")
    
    # 如果 raw 是 None，我們直接給一個空列表，防止 TypeError
    if raw is None:
        data_list = []
    elif isinstance(raw, list):
        data_list = raw
    else:
        data_list = [raw]

    # 顯示表格
    if data_list:
        try:
            # 確保內容是字典，否則轉為字串描述
            processed = [item if isinstance(item, dict) else {"說明": str(item)} for item in data_list]
            df = pd.DataFrame(processed)
            st.table(df)
        except Exception as e:
            st.error(f"表格繪製錯誤: {e}")
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
