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
    if not data:
        st.warning("正在載入數據...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    # 【絕對固化邏輯】
    try:
        # 1. 確保數據是一個列表
        if isinstance(raw, dict):
            data_list = [raw]
        elif isinstance(raw, list):
            data_list = raw
        else:
            data_list = []
            
        # 2. 確保列表中的每個項目都是字典 (過濾掉純字串)
        data_list = [item for item in data_list if isinstance(item, dict)]
        
        # 3. 只有在有資料時才建立 DataFrame
        if data_list:
            df = pd.DataFrame(data_list)
            # 強制處理 index
            df.reset_index(drop=True, inplace=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("目前無籌碼數據。")
            
    except Exception as e:
        st.error(f"表格格式無法解析。")

    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無數據"))

if __name__ == "__main__":
    main()
