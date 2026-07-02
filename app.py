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
        st.warning("⚠️ 正在載入資料中...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 籌碼面：核心修正
    st.subheader("三大法人與籌碼數據")
    raw_data = data.get("institutional_investors")
    
    # 強制將輸入正規化為 list of dicts
    if isinstance(raw_data, dict):
        df_source = [raw_data]
    elif isinstance(raw_data, list):
        df_source = raw_data
    else:
        df_source = []
        
    try:
        # 如果有資料，顯示 DataFrame，否則顯示提示
        if df_source:
            df = pd.DataFrame(df_source)
            # 強制指定 index，避免 ValueError
            df.index = range(len(df))
            st.dataframe(df, use_container_width=True)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.write("資料格式異常，無法轉為表格。")

    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無數據"))

if __name__ == "__main__":
    main()
