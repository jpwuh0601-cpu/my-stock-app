import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def to_float(val):
    """將任何輸入強制轉換為浮點數，並移除所有可能的 Pandas 空值"""
    try:
        # 將字串轉換為 float，若是 None 或 NaN 則統一轉為 0.0
        s_val = str(val)
        if s_val in ['None', 'nan', '<NA>', 'null']:
            return 0.0
        return float(s_val.replace(',', ''))
    except:
        return 0.0

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 這裡增加一個預處理步驟：清洗整個字典
                return data
        except:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("暫無資料，請檢查 GitHub Actions。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：強制使用 to_float 清洗
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{to_float(data.get('price', 0)):,.2f}", delta=f"{to_float(data.get('change', 0)):+.2f}")
    cols[1].metric("每股淨值", f"{to_float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{to_float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{to_float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{to_float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面表格：轉換前強制將 <NA> 替換為 0
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        df = pd.DataFrame(inst_data)
        # 強制將 DataFrame 中所有的 NaN 或 <NA> 替換為 0
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
