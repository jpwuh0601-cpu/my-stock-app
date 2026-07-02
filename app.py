import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    # 強制尋找倉庫根目錄下的 market_data.json
    # 在 Streamlit Cloud 環境中，根目錄通常是 /app/您的專案名稱/
    file_path = "market_data.json"
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"JSON 格式錯誤: {e}")
            return None
    else:
        st.error(f"❌ 找不到檔案: {os.path.abspath(file_path)}")
        st.info("請確認 GitHub Actions 是否已將 market_data.json 推送到 main 分支的根目錄。")
        return None

def main():
    data = load_data()
    if data is None:
        return

    st.title("📈 AI 智能金融監控終端")
    
    # 核心財務指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}", delta=f"{float(data.get('change', 0)):+.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    # 籌碼面分析
    st.subheader("三大法人與籌碼數據")
    try:
        inst_data = data.get("institutional_investors", [])
        if inst_data:
            st.dataframe(pd.DataFrame(inst_data), use_container_width=True)
        else:
            st.write("暫無資料")
    except Exception:
        st.error("資料格式異常，無法顯示表格")

if __name__ == "__main__":
    main()
