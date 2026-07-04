import streamlit as st
import json
import os
import pandas as pd

# 設定頁面配置 (使用 centered 降低初次載入壓力)
st.set_page_config(page_title="AI 專業金融分析終端", layout="centered")

def load_data(filepath):
    """讀取市場數據，防止檔案鎖定"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.title("📈 AI 專業金融分析終端")
    
    # 載入數據
    data = load_data("market_data.json")
    
    # 選股界面
    target = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    info = data.get(target)
    
    if not info:
        st.info("尚未搜尋到資料或資料庫更新中，請確認 GitHub Actions 是否已執行完畢。")
        return

    # 顯示核心數據
    st.metric("即時股價", f"{info.get('price', 0)} 元")
    
    # 顯示基本面摘要
    st.subheader("基本面摘要")
    c1, c2, c3 = st.columns(3)
    c1.metric("淨值 (NAV)", info.get("nav", "N/A"))
    c2.metric("本益比", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    st.subheader("AI 分析摘要")
    st.write(info.get('ai_prediction', '分析中...'))

    if st.checkbox("顯示原始詳細數據"):
        st.json(info)

if __name__ == "__main__":
    main()
