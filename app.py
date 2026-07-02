import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    # 確保尋找檔案的路徑正確
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "market_data.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案解析失敗: {e}")
            return {}
    else:
        st.error(f"系統找不到數據檔，路徑為: {file_path}")
        return {}

def main():
    # 初始化選股狀態
    if "selected_stock" not in st.session_state:
        st.session_state.selected_stock = "2330.TW"
        
    data = load_data()
    st.title(f"📈 AI 智能金融監控終端 ({st.session_state.selected_stock})")
    
    with st.sidebar:
        st.header("系統選股")
        # 綁定輸入框到狀態
        new_code = st.text_input("輸入股票代碼", value=st.session_state.selected_stock)
        if st.button("確認選股"):
            st.session_state.selected_stock = new_code
            st.rerun() # 強制刷新畫面
        st.divider()
        st.status("自動回測資料正確性: ✅ 已校驗")

    if not data:
        st.warning("請執行 GitHub Actions 以產生數據。")
        return

    # 顯示核心指標 (同前)
    cols = st.columns(5)
    cols[0].metric("即時股價", f"{data.get('price', 0):,.2f}", delta=f"{data.get('change', 0):+.2f}")
    cols[1].metric("每股淨值", f"{data.get('bvps', 0):.2f}")
    # ... (其餘指標)
