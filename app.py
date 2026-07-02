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
        except Exception:
            return {}
    return {}

def main():
    data = load_data()
    if not data:
        st.warning("⚠️ 正在載入資料中，請稍候...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 指標區域
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：絕對安全處理
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors")
    
    # 處理三種情況：1. 列表(正確) 2. 字典(單筆資料) 3. 其他(異常)
    try:
        if isinstance(inst_data, list):
            df = pd.DataFrame(inst_data)
        elif isinstance(inst_data, dict):
            # 若是字典，將其轉為單列的 DataFrame
            df = pd.DataFrame([inst_data])
        else:
            df = None
            
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("目前無籌碼數據。")
    except Exception as e:
        st.error(f"表格格式解析異常，原始資料為: {inst_data}")

    # 其他區塊
    st.subheader("AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析"))

if __name__ == "__main__":
    main()
