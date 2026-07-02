import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def get_data_path():
    """獲取與 app.py 同目錄的檔案路徑"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")

def load_data():
    json_path = get_data_path()
    if not os.path.exists(json_path):
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if data is None:
        st.error(f"找不到數據檔案，路徑: {get_data_path()}")
        return

    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    
    # 【關鍵檢查】：檢查 'institutional_investors' 是否存在
    if "institutional_investors" in data and data["institutional_investors"]:
        try:
            raw = data["institutional_investors"]
            df_source = raw if isinstance(raw, list) else [raw]
            df = pd.DataFrame(df_source)
            st.table(df)
        except Exception as e:
            st.error(f"表格格式錯誤: {e}")
    else:
        st.info("目前數據檔案中無 'institutional_investors' 欄位。")
        st.write(f"當前檔案所有可用鍵值: {list(data.keys())}")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 原始數據檢查 (除錯用)"):
        st.json(data)

if __name__ == "__main__":
    main()
