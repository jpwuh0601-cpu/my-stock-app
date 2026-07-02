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
        st.warning("⚠️ 數據檔為空或讀取失敗，請稍候重試。")
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心指標：使用 .get() 加上預設值 0，徹底消除 KeyError
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面：檢查欄位是否存在
    st.subheader("三大法人與籌碼數據")
    
    # 這裡檢查是否真的有 'institutional_investors'，沒有就顯示提示而非崩潰
    if 'institutional_investors' in data and data['institutional_investors']:
        inst_data = data['institutional_investors']
        try:
            df = pd.DataFrame(inst_data)
            st.dataframe(df, width=1000)
        except Exception as e:
            st.error(f"表格格式無法解析: {e}")
    else:
        st.info("目前無籌碼數據資料 (可能尚未完成每日抓取)。")

if __name__ == "__main__":
    main()
