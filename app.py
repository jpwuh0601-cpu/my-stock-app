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
        st.warning("正在等待數據更新...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("即時股價", f"{safe_num(data.get('price', 0)):,.2f}", delta=f"{safe_num(data.get('change', 0)):+.2f}")
    c2.metric("每股淨值", f"{safe_num(data.get('bvps', 0)):.2f}")
    c3.metric("本益比", f"{safe_num(data.get('pe_ratio', 0)):.2f}")
    c4.metric("10日資券比", f"{safe_num(data.get('margin_ratio', 0)):.2f}%")
    c5.metric("預估 EPS", f"{safe_num(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 防禦性籌碼面表格
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    
    # 強制轉換策略：檢查資料類型，並使用 json_normalize 進行結構化處理
    if inst_data:
        try:
            # 確保資料是 list 且不是 Series 物件
            if isinstance(inst_data, dict):
                inst_data = [inst_data]
            
            # 使用 json_normalize 解決結構不一致的 Series/Dict 混合問題
            df = pd.json_normalize(inst_data)
            
            # 最後檢查是否為空，並填充 0
            st.dataframe(df.fillna(0), use_container_width=True)
        except Exception as e:
            st.error(f"表格格式異常，無法解析: {e}")
            st.write(inst_data)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
