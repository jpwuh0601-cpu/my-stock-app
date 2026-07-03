import streamlit as st
import pandas as pd
import json
import os

# 設定頁面佈局
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """安全讀取市場資料"""
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"資料讀取錯誤: {e}")
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    
    data = load_data()
    # 確保代號清單正確
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    # 側邊欄設計
    with st.sidebar:
        st.subheader("選股搜尋")
        user_input = st.text_input("輸入股票代號 (例如: 2330.TW)")
        
        # 修正：確保按下按鈕後更新 Session State
        if st.button("確定選股"):
            st.session_state.target = user_input
    
    # 優先顯示 Session 中的目標，否則預設為第一個
    target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(target, {})

    if info:
        st.subheader(f"目標股票: {target}")
        
        # 顯示籌碼數據
        if "institutional_daily" in info:
            st.subheader("三大法人 10 日買賣超細項")
            st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
            
        if "broker_daily" in info:
            st.subheader("10 家主力券商 10 日買賣超細項")
            st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)
    else:
        st.warning(f"目前查無代號 '{target}' 的數據，請確認 GitHub Actions 已執行且資料檔已更新。")

if __name__ == "__main__":
    main()
