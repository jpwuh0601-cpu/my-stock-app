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
    
    # 核心指標
    st.metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    st.subheader("🏦 三大法人與籌碼數據")
    raw = data.get("institutional_investors")

    # 極致穩定的呈現方式：檢查並強制轉換
    try:
        # 如果 raw 是字典，轉列表
        if isinstance(raw, dict):
            raw = [raw]
        
        # 如果 raw 不是列表 (例如 None 或其他)，給予空列表
        if not isinstance(raw, list):
            raw = []

        # 顯示資料
        if len(raw) > 0:
            # 建立 DataFrame 前，先確保每一個項目都是字典
            df = pd.DataFrame([item if isinstance(item, dict) else {"內容": str(item)} for item in raw])
            # 使用 st.table 代替 st.dataframe，它對於複雜結構容錯性更高
            st.table(df)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error("表格解析發生意外，已轉為原始文字呈現：")
        st.write(raw)

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

    with st.expander("🔍 除錯數據結構"):
        st.write("原始資料類型:", type(raw))
        st.json(raw)

if __name__ == "__main__":
    main()
