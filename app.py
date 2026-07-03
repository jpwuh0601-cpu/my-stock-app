import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"JSON 讀取失敗: {e}")
    return {}

def render_dataframe(data, title):
    """防彈表格渲染器"""
    if not data:
        st.write(f"{title}: 暫無數據")
        return
    
    try:
        # 如果是 list 且內部有 dict，直接轉換
        if isinstance(data, list):
            df = pd.DataFrame(data)
            st.subheader(title)
            st.dataframe(df, width=None)
        else:
            st.write(f"{title}: 資料格式非表格類型，請檢查 worker.py 輸出")
    except Exception as e:
        st.warning(f"無法顯示表格: {e}")

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("尚未讀取到數據，請等待 GitHub Actions 下次更新。")
        return

    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        st.subheader("選股搜尋")
        target = st.selectbox("選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    current_target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(current_target, {})
    
    if info:
        st.subheader(f"分析目標: {current_target}")
        # 進行安全渲染
        render_dataframe(info.get("institutional_daily"), "三大法人 10 日買賣超")
        render_dataframe(info.get("broker_daily"), "主力券商 10 日買賣超")
    else:
        st.write("請選擇股票。")

if __name__ == "__main__":
    main()
