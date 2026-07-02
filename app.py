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
    
    # 核心指標：簡單安全讀取
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面：不使用 DataFrame，改用「最原始的字典列表顯示法」
    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    if isinstance(raw, list) and len(raw) > 0:
        # 使用 Markdown 表格語法，完全繞過 Pandas
        st.markdown("| 機構 | 買賣超 |")
        st.markdown("| --- | --- |")
        for item in raw:
            org = item.get("機構", "未知")
            val = item.get("買賣超", 0)
            st.markdown(f"| {org} | {val} |")
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯數據"):
        st.json(data)

if __name__ == "__main__":
    main()
