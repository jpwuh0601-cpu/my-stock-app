import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📊 AI 智能投資決策儀表板")
    data = load_data()
    
    price = data.get("price", 0)
    change = data.get("change", 0)
    
    # 核心指標：加入 delta 參數實現漲紅跌綠
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(price):,.2f}", delta=f"{float(change):.2f}")
    
    # ... (其餘 UI 保持不變)
    # 籌碼表格區塊
    st.subheader("三大法人買賣超")
    df_inst = pd.DataFrame(data.get("institutional_investors", []))
    if not df_inst.empty:
        st.dataframe(df_inst, use_container_width=True, hide_index=True)

    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "分析準備中..."))

if __name__ == "__main__":
    main()
