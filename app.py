import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

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
        st.warning("暫無資料，請檢查 GitHub Actions 是否執行完畢。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # --- 關鍵修正：強制將所有數據轉換為數值，並處理可能存在的錯誤 ---
    def to_num(val):
        try:
            return float(val)
        except:
            return 0.0

    price = to_num(data.get('price', 0))
    change = to_num(data.get('change', 0))
    bvps = to_num(data.get('bvps', 0))
    pe = to_num(data.get('pe_ratio', 0))
    margin = to_num(data.get('margin_ratio', 0))
    eps = to_num(data.get('eps_forecast', 0))

    # --- 頁面渲染 ---
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{price:,.2f}", delta=f"{change:+.2f}")
    cols[1].metric("每股淨值", f"{bvps:.2f}")
    cols[2].metric("本益比", f"{pe:.2f}")
    cols[3].metric("10日資券比", f"{margin:.2f}%")
    cols[4].metric("預估 EPS", f"{eps:.2f}")
    
    st.divider()

    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
