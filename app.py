import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def get_value(data, key, default=0.0):
    """強大的數據清理函式：確保取出的值永遠是 float 或字串"""
    val = data.get(key, default)
    try:
        # 如果是列表或字典，回傳預設值
        if isinstance(val, (list, dict)):
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

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
        st.warning("暫無資料，請檢查 GitHub Actions 是否執行成功。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 使用 get_value 清理後的數據進行渲染
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{get_value(data, 'price'):,.2f}", delta=f"{get_value(data, 'change'):+.2f}")
    cols[1].metric("每股淨值", f"{get_value(data, 'bvps'):.2f}")
    cols[2].metric("本益比", f"{get_value(data, 'pe_ratio'):.2f}")
    cols[3].metric("10日資券比", f"{get_value(data, 'margin_ratio'):.2f}%")
    cols[4].metric("預估 EPS", f"{get_value(data, 'eps_forecast'):.2f}")
    
    st.divider()

    # 籌碼面分析
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    if isinstance(inst_data, list):
        st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
    else:
        st.info("暫無法人籌碼數據")

if __name__ == "__main__":
    main()
