import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def safe_float(value, default=0.0):
    """安全轉換浮點數，防止數據格式異常導致崩潰"""
    try:
        if value is None: return default
        return float(value)
    except (ValueError, TypeError):
        return default

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "market_data.json")
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
        st.warning("暫無資料，請等待 GitHub Actions 更新。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心財務指標：使用 safe_float 強制清洗數據
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{safe_float(data.get('price')):,.2f}", delta=f"{safe_float(data.get('change')):+.2f}")
    cols[1].metric("每股淨值", f"{safe_float(data.get('bvps')):.2f}")
    cols[2].metric("本益比", f"{safe_float(data.get('pe_ratio')):.2f}")
    cols[3].metric("10日資券比", f"{safe_float(data.get('margin_ratio')):.2f}%")
    cols[4].metric("預估 EPS", f"{safe_float(data.get('eps_forecast')):.2f}")
    
    st.divider()

    # 籌碼面分析
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list) and len(inst_data) > 0:
        st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
