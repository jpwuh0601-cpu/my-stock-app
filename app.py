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
    
    # 顯示即時股價
    price = data.get("price", 0.0)
    st.metric("即時股價", f"{float(price):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 獲取資料
    raw = data.get("institutional_investors")
    
    # 這裡實作最嚴格的索引處理邏輯
    # 1. 確保 raw 不為 None
    # 2. 強制將單一字典轉為列表
    # 3. 強制指派 index，徹底解決 Scalar ValueError
    try:
        if raw is not None:
            processed_data = raw if isinstance(raw, list) else [raw]
            
            if processed_data:
                # 關鍵修正： explicitly provide index
                df = pd.DataFrame(processed_data, index=range(len(processed_data)))
                st.table(df)
            else:
                st.info("目前無籌碼數據。")
        else:
            st.info("數據欄位為空。")
    except Exception as e:
        st.error(f"表格格式解析異常: {e}")
        st.write("原始數據內容:", raw)

    st.subheader("🤖 AI 智能分析")
    st.write(str(data.get("ai_prediction", "暫無分析數據。")))

    with st.expander("🔍 除錯數據檢查"):
        st.json(data)

if __name__ == "__main__":
    main()
