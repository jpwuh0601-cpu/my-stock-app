import streamlit as st
import pandas as pd
import json
import os
import numpy as np

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def clean_data(data):
    """將字典中所有 NaN 或無效值替換為安全值"""
    if isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(v) for v in data]
    elif isinstance(data, float) and np.isnan(data):
        return 0.0
    return data

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return clean_data(raw_data) # 進行清洗
        except:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("暫無資料，請檢查 GitHub Actions。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 使用清洗過的 data 進行渲染
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}", delta=f"{float(data.get('change', 0)):+.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    st.subheader("三大法人與籌碼數據")
    # 將所有數據轉為 DataFrame 前進行最後一次 fillna(0)
    inst_df = pd.DataFrame(data.get("institutional_investors", []))
    if not inst_df.empty:
        st.dataframe(inst_df.fillna(0), use_container_width=True)
    else:
        st.info("暫無法人籌碼數據")

if __name__ == "__main__":
    main()
