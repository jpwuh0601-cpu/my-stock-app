import streamlit as st
import pandas as pd
import json
import os

def load_data():
    # 強制檢查檔案是否存在與路徑
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案格式錯誤: {e}")
            return {}
    else:
        st.warning(f"找不到數據檔案: {os.getcwd()}/{file_path}")
        return {}

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    st.title("📊 AI 智能金融終端")
    
    data = load_data()
    
    if not data:
        st.error("目前沒有資料，請確認 GitHub Actions 是否執行成功並正確推送 market_data.json")
        return

    # 頂部即時監控
    price = data.get("price", 0)
    change = data.get("change", 0)
    
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(price):,.2f}", delta=f"{float(change):.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[3].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    # 籌碼面分析
    st.subheader("三大法人與籌碼數據")
    df_inst = pd.DataFrame(data.get("institutional_investors", []))
    if not df_inst.empty:
        st.dataframe(df_inst, use_container_width=True)
    
    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "分析中..."))

if __name__ == "__main__":
    main()
