import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """讀取市場數據"""
    json_path = "market_data.json"
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    data = load_data()
    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：防禦式讀取，若無則顯示 0
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面：防禦式呈現，若無欄位則顯示提示
    st.subheader("🏦 三大法人與籌碼數據")
    
    if "institutional_investors" in data:
        raw = data["institutional_investors"]
        try:
            # 強制轉換並處理
            df_source = raw if isinstance(raw, list) else [raw]
            df = pd.DataFrame(df_source)
            st.table(df)
        except Exception as e:
            st.error(f"表格格式無法解析: {e}")
    else:
        st.warning("目前數據來源中沒有 'institutional_investors' 欄位。")
        st.info(f"現有數據可用鍵值: {list(data.keys())}")

    # AI 分析
    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無 AI 分析結果。"))

    # 除錯區塊
    with st.expander("🔍 除錯：查看完整數據內容"):
        st.json(data)

if __name__ == "__main__":
    main()
