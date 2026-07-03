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
    
    # 股價與分析
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.subheader("🏦 三大法人籌碼數據")
    raw = data.get("institutional_investors")
    
    # 核心修正：將所有輸入強制正規化為 [ {"欄位": "值"} ] 的列表
    normalized_data = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                normalized_data.append(item)
            else:
                normalized_data.append({"內容": str(item)})
    elif isinstance(raw, dict):
        normalized_data.append(raw)
    elif raw is not None:
        normalized_data.append({"內容": str(raw)})

    if normalized_data:
        try:
            # 指定 Index 且不依賴自動推導
            df = pd.DataFrame(normalized_data, index=range(len(normalized_data)))
            st.table(df)
        except Exception as e:
            st.error(f"表格格式異常: {e}")
            st.write("Debug:", normalized_data)
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
