import streamlit as st
import pandas as pd
import json
import os
import math

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def safe_numeric(val):
    """
    極致防禦：確保任何輸入都能安全轉為 float，
    如果輸入為空字串、None 或無效內容，一律回傳 0.0。
    """
    if val is None: return 0.0
    try:
        # 強制移除所有空格與千分位符號，若轉為字串後為空，回傳 0.0
        str_val = str(val).strip().replace(',', '')
        if not str_val or str_val == "": return 0.0
        
        f = float(str_val)
        return 0.0 if math.isnan(f) or math.isinf(f) else f
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
    
    # 核心指標：使用 safe_numeric 處理所有輸入
    p = safe_numeric(data.get('price'))
    c = safe_numeric(data.get('change'))
    b = safe_numeric(data.get('bvps'))
    pe = safe_numeric(data.get('pe_ratio'))
    m = safe_numeric(data.get('margin_ratio'))
    e = safe_numeric(data.get('eps_forecast'))

    cols = st.columns(5)
    cols[0].metric("即時股價", f"{p:,.2f}", delta=f"{c:+.2f}")
    cols[1].metric("每股淨值", f"{b:.2f}")
    cols[2].metric("本益比", f"{pe:.2f}")
    cols[3].metric("10日資券比", f"{m:.2f}%")
    cols[4].metric("預估 EPS", f"{e:.2f}")
    
    st.divider()

    # 籌碼面：針對 DataFrame 做最終清洗
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list) and len(inst_data) > 0:
        df = pd.DataFrame(inst_data)
        # 強制將整個表格轉換為數值，非數值欄位轉為 0
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暫無法人籌碼數據")

if __name__ == "__main__":
    main()
