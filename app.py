import streamlit as st
import pandas as pd
import json
import os
import math

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def safe_num(val):
    """強大的數值清洗：若為 NaN 或 None 或無法轉換，一律回傳 0.0"""
    try:
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val):
            return 0.0
        return f_val
    except:
        return 0.0

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
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
    
    # 核心指標：全部經過 safe_num 處理
    p = safe_num(data.get('price'))
    c = safe_num(data.get('change'))
    b = safe_num(data.get('bvps'))
    pe = safe_num(data.get('pe_ratio'))
    m = safe_num(data.get('margin_ratio'))
    e = safe_num(data.get('eps_forecast'))

    cols = st.columns(5)
    cols[0].metric("即時股價", f"{p:,.2f}", delta=f"{c:+.2f}")
    cols[1].metric("每股淨值", f"{b:.2f}")
    cols[2].metric("本益比", f"{pe:.2f}")
    cols[3].metric("10日資券比", f"{m:.2f}%")
    cols[4].metric("預估 EPS", f"{e:.2f}")
    
    st.divider()

    # 籌碼面：針對 DataFrame 做最後檢查
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        df = pd.DataFrame(inst_data)
        # 強制將 DataFrame 中所有的 NaN 轉為 0
        df = df.fillna(0)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
