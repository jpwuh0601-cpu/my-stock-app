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
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 關鍵防禦：若資料為 None，則回傳空字典
                return data if data is not None else {}
        except Exception as e:
            st.error(f"檔案解析失敗: {e}")
            return {}
    return {}

def main():
    data = load_data()
    # 防禦性檢查
    if not isinstance(data, dict):
        st.warning("數據格式異常，無法顯示。")
        return
        
    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：即使資料不存在，儀表板也會顯示 0 而不崩潰
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{safe_num(data.get('price', 0)):,.2f}", delta=f"{safe_num(data.get('change', 0)):+.2f}")
    cols[1].metric("每股淨值", f"{safe_num(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{safe_num(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{safe_num(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{safe_num(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面表格
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    
    if isinstance(inst_data, list) and len(inst_data) > 0:
        try:
            df = pd.DataFrame(inst_data).fillna(0)
            st.dataframe(df, use_container_width=True)
        except:
            st.info("籌碼數據格式無法轉換為表格。")
    else:
        st.info("暫無法人籌碼數據")

if __name__ == "__main__":
    main()
