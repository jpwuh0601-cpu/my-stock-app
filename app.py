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
    
    # 核心指標 (防禦性存取)
    price = float(data.get("price", 0))
    st.metric("即時股價", f"{price:,.2f}")
    
    st.divider()

    # 籌碼面：極致防禦處理
    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    try:
        # 強制正規化：確保它是列表，並且裡面都是字典
        if isinstance(raw, dict):
            proc_data = [raw]
        elif isinstance(raw, list):
            proc_data = raw
        else:
            proc_data = []

        # 二次防禦：清洗掉非字典的雜訊
        clean_data = []
        for item in proc_data:
            if isinstance(item, dict):
                # 強制將所有 value 轉字串，避免型別不一致導致的建構錯誤
                clean_data.append({str(k): str(v) for k, v in item.items()})
        
        if clean_data:
            # 建立表格並明確指定 index
            df = pd.DataFrame(clean_data)
            df.index = range(len(df))
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("目前無籌碼數據。")
            
    except Exception as e:
        st.error(f"數據結構無法解析: {e}")
        st.write("原始資料:", raw)

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯：查看完整 JSON 內容"):
        st.json(data)

if __name__ == "__main__":
    main()
