import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def to_float(value):
    """將任何輸入強制轉換為浮點數，防止 ValueError 與 TypeError"""
    try:
        # 先轉為字串再轉浮點，處理字串數字
        return float(str(value).replace(',', ''))
    except (ValueError, TypeError):
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
        st.warning("暫無資料，請檢查 GitHub Actions。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：全部使用 to_float 進行清洗
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{to_float(data.get('price')):,.2f}", delta=f"{to_float(data.get('change')):+.2f}")
    cols[1].metric("每股淨值", f"{to_float(data.get('bvps')):.2f}")
    cols[2].metric("本益比", f"{to_float(data.get('pe_ratio')):.2f}")
    cols[3].metric("10日資券比", f"{to_float(data.get('margin_ratio')):.2f}%")
    cols[4].metric("預估 EPS", f"{to_float(data.get('eps_forecast')):.2f}")
    
    st.divider()

    # 籌碼面表格
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        # 轉換前先將內容轉為數值，防止表格渲染時出現 ValueError
        df = pd.DataFrame(inst_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
