import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

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
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：強制結構重組
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors", [])
    
    if isinstance(inst_data, list) and len(inst_data) > 0:
        # 【強制清洗邏輯】：將資料轉換為純粹的列表字典，過濾掉任何非標準物件
        sanitized_data = []
        for item in inst_data:
            if isinstance(item, dict):
                # 只保留可以轉為字串/數值的內容，過濾掉複雜物件
                clean_item = {str(k): str(v) for k, v in item.items()}
                sanitized_data.append(clean_item)
        
        # 轉換為 DataFrame，且不進行複雜的類型推斷
        df = pd.DataFrame(sanitized_data)
        st.dataframe(df, width=1000)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
