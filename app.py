import streamlit as st
import pandas as pd
import json
import os  # 正確的匯入方式：這是一個獨立的標準模組，不要寫在 streamlit 後面

# 設定頁面佈局
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """使用絕對路徑讀取數據，確保穩定性"""
    # 取得當前檔案所在的目錄
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "market_data.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取 JSON 發生錯誤: {e}")
            return {}
    else:
        st.error(f"找不到檔案: {file_path}")
        return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    
    # 載入資料
    data = load_data()
    
    if not data:
        st.info("尚未載入數據，請確認 GitHub Actions 是否執行成功。")
        return

    # 簡單測試：顯示資料字典的 keys，證明讀取成功
    tickers = [t for t in data.keys() if t != "last_updated"]
    st.write("已成功載入以下股票資料:", tickers)

if __name__ == "__main__":
    main()
