import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據，增加嚴格的格式驗證"""
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
    
    # 核心指標顯示
    price = data.get("price", 0)
    st.metric("即時股價", f"{float(price):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人籌碼數據")
    
    # 取得原始數據
    raw = data.get("institutional_investors")
    
    # 【絕對防禦】：確保 raw 是列表且內容為字典
    try:
        if raw is not None:
            # 若為單一字典，強制轉為列表
            data_list = raw if isinstance(raw, list) else [raw]
            
            # 若列表內元素非字典，強制轉為字典結構，避免 ValueError
            processed_data = []
            for item in data_list:
                if isinstance(item, dict):
                    processed_data.append(item)
                else:
                    processed_data.append({"說明": str(item)})
            
            # 【關鍵修復】：明確傳入 index，這能徹底解決 scalar values 報錯
            if processed_data:
                df = pd.DataFrame(processed_data, index=range(len(processed_data)))
                st.table(df)
            else:
                st.info("暫無籌碼數據。")
        else:
            st.info("數據欄位為空。")
            
    except Exception as e:
        st.error(f"表格繪製錯誤: {e}")
        st.write("原始資料:", raw)

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯數據結構"):
        st.json(data)

if __name__ == "__main__":
    main()
