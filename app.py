import streamlit as st
import pandas as pd
import json
import os

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    data = load_data()
    
    st.title("📈 AI 智能金融監控終端")
    
    # 核心財務指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    cols[2].metric("本益比", f"{data.get('pe_ratio', 0):.2f}")
    cols[3].metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")
    cols[4].metric("預估 EPS", f"{data.get('eps_forecast', 0):.2f}")
    
    st.divider()

    # 安全地轉換籌碼數據
    st.subheader("三大法人與籌碼數據")
    
    # 這裡將 list 強制轉為 DataFrame，如果為空則顯示空表格
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        df_inst = pd.DataFrame(inst_data)
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.write("法人數據格式異常")

    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "分析中..."))

if __name__ == "__main__":
    main()
