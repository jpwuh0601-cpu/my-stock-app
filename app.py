import streamlit as st
import pandas as pd
import json
import os
import numpy as np

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def preprocess_data(data):
    """全域數據預處理：將所有不安全的格式轉為標準化格式"""
    if isinstance(data, dict):
        return {k: preprocess_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [preprocess_data(v) for v in data]
    elif isinstance(data, float):
        if np.isnan(data) or np.isinf(data):
            return 0.0
        return data
    return data

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return preprocess_data(raw_data) # 在載入後立即清洗
        except:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("正在等待數據更新...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：經過 preprocess_data 清洗，絕對安全
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}", delta=f"{data.get('change', 0):+.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    cols[2].metric("本益比", f"{data.get('pe_ratio', 0):.2f}")
    cols[3].metric("10日資券比", f"{data.get('margin_ratio', 0):.2f}%")
    cols[4].metric("預估 EPS", f"{data.get('eps_forecast', 0):.2f}")
    
    st.divider()

    # 籌碼面：經過預處理的 DataFrame 絕對不會有 NaN
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list) and len(inst_data) > 0:
        df = pd.DataFrame(inst_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
