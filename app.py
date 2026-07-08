import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

def load_data():
    """只讀取本地檔案，絕不觸發網路請求"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案讀取錯誤: {e}")
            return {}
    return {}

def main():
    st.title("📈 專業股市決策儀表板")
    
    # 讀取本地資料
    data = load_data()
    
    # 取得代號列表
    tickers = list(data.keys()) if data else []
    
    st.subheader("🛠️ 決策標的選擇")
    ticker = st.selectbox("請選擇您的自選股", tickers if tickers else ["無數據"])
    
    if st.button("確定選股查詢"):
        st.session_state.current_ticker = ticker
    
    target = st.session_state.get("current_ticker", ticker if tickers else None)
    
    if target and target in data:
        s = data[target]
        st.subheader(f"📊 決策報告：{target}")
        
        # 顯示各項數據
        st.metric("即時股價", s.get('price', 0))
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", s.get('nav', 0))
        c2.metric("本益比", s.get('pe', 0))
        c3.metric("EPS", s.get('eps', 0))
        
        # 顯示警示與新聞
        st.subheader("📰 市場動態與警示")
        st.info(f"地緣政治警示: {s.get('black_swan', '目前安全')}")
        st.success(f"AI 財報預測: {s.get('ai_prediction', '分析中...')}")
        
    else:
        st.warning("目前沒有數據。請檢查 market_data.json 是否已存在，或執行 main_task.py 更新數據。")

if __name__ == "__main__":
    main()
