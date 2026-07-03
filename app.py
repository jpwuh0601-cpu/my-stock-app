import streamlit as st
import pandas as pd
import json
import os

# 強制設定頁面寬度，避免載入時跑版
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """安全讀取市場資料，並回傳錯誤訊息以便除錯"""
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return None, f"找不到檔案: {file_path}"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data, None
    except Exception as e:
        return None, f"JSON 解析失敗: {str(e)}"

def main():
    st.title("📈 AI 智能金融監控終端")
    
    # 載入資料並顯示錯誤
    data, error = load_data()
    
    if error:
        st.error(f"系統錯誤: {error}")
        st.write("請確認 GitHub Actions 是否有成功寫入 market_data.json。")
        return
        
    st.success("資料載入成功！")
    
    # 簡單測試顯示，確保邏輯沒有卡住
    tickers = list(data.keys())
    selected = st.selectbox("請選擇股票", tickers)
    st.write(data[selected])

if __name__ == "__main__":
    main()
