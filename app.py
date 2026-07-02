import streamlit as st
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
    
    # 顯示股價
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    # 極致防禦模式：不使用 pd.DataFrame，直接用原始字典列表呈現
    if isinstance(raw, list) and len(raw) > 0:
        # 手動將列表轉換成顯示表格
        st.table(raw)
    elif isinstance(raw, dict):
        # 如果只有一筆資料，轉成清單顯示
        st.table([raw])
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯數據結構"):
        st.write("原始資料:", raw)
        st.json(data)

if __name__ == "__main__":
    main()
