import streamlit as st
import pandas as pd
import json
import os
import math

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def safe_num(val):
    """
    極致過濾：若遇到列表、字典或其他非單一數值，
    嘗試提取第一個元素或強制轉 0.0。
    """
    try:
        # 如果是列表，提取第一個元素
        if isinstance(val, list):
            val = val[0] if len(val) > 0 else 0.0
        
        f = float(val)
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
    
    # 核心指標：強制透過 safe_num 清洗，解決列表衝突問題
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("即時股價", f"{safe_num(data.get('price', 0)):,.2f}", delta=f"{safe_num(data.get('change', 0)):+.2f}")
    c2.metric("每股淨值", f"{safe_num(data.get('bvps', 0)):.2f}")
    c3.metric("本益比", f"{safe_num(data.get('pe_ratio', 0)):.2f}")
    c4.metric("10日資券比", f"{safe_num(data.get('margin_ratio', 0)):.2f}%")
    c5.metric("預估 EPS", f"{safe_num(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：確保表格顯示前已過濾所有非數值
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        df = pd.DataFrame(inst_data)
        # 移除任何無法轉為數值的欄位，保證表格顯示安全
        st.dataframe(df.astype(str), use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
