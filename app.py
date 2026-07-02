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
        st.warning("⚠️ 正在載入市場資料，請稍候...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標顯示
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    # 【絕對固化邏輯】：強制處理標量與索引問題
    try:
        # 確保資料是 List of Dicts
        if isinstance(raw, dict):
            df_source = [raw]
        elif isinstance(raw, list):
            df_source = raw
        else:
            df_source = []

        # 顯示資料
        if df_source:
            # 建立 DataFrame 並明確指定 index=range(len(df_source))
            # 這是解決 "must pass an index" 的關鍵做法
            df = pd.DataFrame(df_source, index=range(len(df_source)))
            
            # 使用 table 顯示更穩定，且不隱藏 index 避免結構混亂
            st.table(df)
        else:
            st.info("目前無籌碼數據。")
            
    except Exception as e:
        st.error(f"表格格式異常: {e}")
        st.write("原始資料類型:", type(raw))

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯：查看完整數據內容"):
        st.json(data)

if __name__ == "__main__":
    main()
