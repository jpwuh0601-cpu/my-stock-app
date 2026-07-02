import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def get_float(val, default=0.0):
    try:
        return float(val)
    except:
        return default

def load_data():
    path = "market_data.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
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
    
    # 核心指標
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("即時股價", f"{get_float(data.get('price')):,.2f}", delta=f"{get_float(data.get('change')):+.2f}")
    c2.metric("每股淨值", f"{get_float(data.get('bvps')):.2f}")
    c3.metric("本益比", f"{get_float(data.get('pe_ratio')):.2f}")
    c4.metric("10日資券比", f"{get_float(data.get('margin_ratio')):.2f}%")
    c5.metric("預估 EPS", f"{get_float(data.get('eps_forecast')):.2f}")

    # 財務報表區域 (加入容錯檢測)
    st.subheader("今年與去年每季財務報表")
    financials = data.get("financials", {})
    if isinstance(financials, dict) and len(financials) > 0:
        try:
            # 嘗試轉換為表格
            df_fin = pd.DataFrame.from_dict(financials, orient='index')
            st.table(df_fin)
        except:
            st.write(financials) # 若轉表失敗，直接輸出原始字典
    else:
        st.info("尚無財報數據")

    # 籌碼面
    st.subheader("三大法人 10日買賣超")
    inst = data.get("institutional_investors", [])
    if isinstance(inst, list) and len(inst) > 0:
        st.dataframe(pd.DataFrame(inst), use_container_width=True)
    else:
        st.info("暫無籌碼數據")

if __name__ == "__main__":
    main()
