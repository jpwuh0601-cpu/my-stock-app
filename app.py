import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    # 1. 定義我們期望的路徑
    target_filename = "market_data.json"
    
    # 2. 列出當前環境的所有檔案 (除錯用)
    files_in_current_dir = os.listdir('.')
    
    # 3. 嘗試讀取檔案
    if os.path.exists(target_filename):
        try:
            with open(target_filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案存在但讀取錯誤: {e}")
            return {}
    else:
        # 當找不到檔案時，將除錯資訊顯示在頁面上
        st.error(f"❌ 系統找不到 {target_filename} 檔案！")
        st.write("--- 除錯資訊 ---")
        st.write(f"當前工作目錄: {os.getcwd()}")
        st.write(f"目錄下的所有檔案: {files_in_dir}")
        st.info("請檢查 GitHub Actions 是否確實執行成功，並且成功執行了 'git push' 將該檔案推送到倉庫根目錄。")
        return {}

def main():
    data = load_data()
    if not data:
        return # 若沒數據則停止渲染

    st.title("📈 AI 智能金融監控終端")
    
    # 核心財務指標
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}", delta=f"{float(data.get('change', 0)):+.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("本益比", f"{float(data.get('pe_ratio', 0)):.2f}")
    cols[3].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[4].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
    
    st.divider()

    st.subheader("籌碼與主力分析")
    st.dataframe(pd.DataFrame(data.get("institutional_investors", [])), use_container_width=True)

if __name__ == "__main__":
    main()
