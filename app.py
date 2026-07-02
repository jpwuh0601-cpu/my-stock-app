import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取數據，使用絕對路徑"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案解析失敗: {e}")
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 核心指標
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    # 絕對防禦機制
    try:
        if raw:
            # 強制處理成列表結構
            data_list = raw if isinstance(raw, list) else [raw]
            
            # 強制轉換：如果項目不是字典，轉為字典
            clean_list = [item if isinstance(item, dict) else {"數據": str(item)} for item in data_list]
            
            # 【關鍵修正】：強制指定索引，並確保 DataFrame 讀取無誤
            df = pd.DataFrame(clean_list, index=range(len(clean_list)))
            
            st.table(df)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error(f"表格格式解析異常: {e}")
        st.write("原始資料內容:", raw)

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯數據結構"):
        st.json(data)

if __name__ == "__main__":
    main()
