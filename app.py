import streamlit as st
import pandas as pd
import json
import os
import math

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def safe_num(val):
    try:
        f = float(val)
        return 0.0 if math.isnan(f) or math.isinf(f) else f
    except:
        return 0.0

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
        st.warning("暫無資料，請等待系統抓取。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("即時股價", f"{safe_num(data.get('price')):,.2f}", delta=f"{safe_num(data.get('change')):+.2f}")
    c2.metric("每股淨值", f"{safe_num(data.get('bvps')):.2f}")
    c3.metric("本益比", f"{safe_num(data.get('pe_ratio')):.2f}")
    c4.metric("10日資券比", f"{safe_num(data.get('margin_ratio')):.2f}%")
    c5.metric("預估 EPS", f"{safe_num(data.get('eps_forecast')):.2f}")
    
    st.divider()

    # 防禦性籌碼面表格
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    
    # 強制將資料轉為標準的扁平化字典列表
    if isinstance(inst_data, list) and len(inst_data) > 0:
        try:
            df = pd.json_normalize(inst_data) # 使用 json_normalize 解決巢狀結構問題
            st.dataframe(df.fillna(0), use_container_width=True)
        except Exception as e:
            st.write("資料格式異常，無法顯示表格：", inst_data)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
