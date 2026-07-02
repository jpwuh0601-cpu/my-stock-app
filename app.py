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
        st.warning("正在等待數據更新...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標顯示 (使用 get 預設值避免 KeyError)
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    cols[2].metric("本益比", f"{data.get('pe_ratio', 0):.2f}")
    cols[3].metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")
    cols[4].metric("預估 EPS", f"{data.get('eps_forecast', 0):.2f}")
    
    st.divider()

    # 籌碼面：強制清洗數據
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    
    if inst_data:
        # 1. 轉為 DataFrame
        df = pd.DataFrame(inst_data)
        
        # 2. 強制將所有欄位轉為數字，無法轉換的 (例如空字串 '') 自動變為 NaN
        # 3. 用 fillna(0) 將 NaN 全部補 0，徹底解決 ValueError
        for col in df.columns:
            if col != '機構': # '機構' 欄位是文字，跳過
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        st.dataframe(df, width=1000)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
