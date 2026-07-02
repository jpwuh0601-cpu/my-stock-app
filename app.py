import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = "market_data.json"
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
    
    # 顯示核心指標
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 針對確認存在的欄位進行處理
    raw = data.get("institutional_investors", [])
    
    if isinstance(raw, list) and len(raw) > 0:
        # 手動處理每一筆數據，確保每一個欄位都是扁平的 (Flatten)
        flattened_data = []
        for item in raw:
            if isinstance(item, dict):
                # 如果項目裡還有巢狀結構，我們會把它壓平
                row = {str(k): str(v) for k, v in item.items()}
                flattened_data.append(row)
        
        if flattened_data:
            df = pd.DataFrame(flattened_data)
            st.table(df)
        else:
            st.info("資料結構無法解析。")
    else:
        st.info("目前無籌碼數據資料。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

if __name__ == "__main__":
    main()
