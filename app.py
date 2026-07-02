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
            return None
    return None

def main():
    data = load_data()
    if not data:
        st.warning("正在等待數據更新...")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標 (增加錯誤處理)
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：採用「絕對防護模式」
    st.subheader("三大法人與籌碼數據")
    inst_data = data.get("institutional_investors")
    
    # 防護邏輯：如果不符合列表結構，絕對不丟進 DataFrame
    if isinstance(inst_data, list) and len(inst_data) > 0:
        try:
            df = pd.DataFrame(inst_data)
            # 確保內容是二維的
            if df.ndim == 2:
                st.dataframe(df, width=1000)
            else:
                st.text(f"數據結構異常，無法顯示表格: {inst_data}")
        except Exception:
            st.text(f"數據解析失敗，顯示原始資料: {inst_data}")
    else:
        st.info("籌碼數據缺失，請稍候重試。")

if __name__ == "__main__":
    main()
