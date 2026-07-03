import streamlit as st
import pandas as pd
import json
import os

# 設定頁面與版面
st.set_page_config(layout="wide", page_title="AI 金融監控系統")

# 使用絕對路徑讀取，確保在任何執行環境下都能找到檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """嘗試讀取資料，並返回詳細狀態"""
    if not os.path.exists(DATA_PATH):
        return None, f"檔案路徑錯誤: {DATA_PATH} 不存在。"
    
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data, None
    except Exception as e:
        return None, f"讀取 JSON 發生錯誤: {str(e)}"

def main():
    st.title("📈 AI 智能金融監控終端")
    
    # 顯示除錯路徑，幫助排查環境問題
    st.sidebar.caption(f"數據路徑: {DATA_PATH}")
    
    data, error = load_data()
    
    if error:
        st.error(error)
        st.info("請檢查 GitHub Actions 是否確實成功產生了 market_data.json。")
        return

    # 成功載入後顯示資料
    tickers = [t for t in data.keys() if t != "last_updated"]
    if not tickers:
        st.warning("數據庫為空，請等待下次自動化排程更新。")
        return

    target = st.sidebar.selectbox("選擇股票", tickers)
    info = data.get(target, {})

    st.subheader(f"分析目標: {target}")
    st.json(info) # 暫時用 JSON 格式顯示所有資料，以驗證是否讀取成功

if __name__ == "__main__":
    main()
