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
            st.error(f"解析 JSON 錯誤: {e}")
    return {}

def safe_display_df(data_key, info, title):
    """安全地顯示表格，如果格式不對則跳過並顯示除錯資訊"""
    raw_data = info.get(data_key)
    if raw_data:
        try:
            # 強制將資料轉換為 list of dicts，避免錯誤格式
            df = pd.DataFrame(raw_data)
            st.subheader(title)
            st.dataframe(df, width=None)
        except Exception as e:
            st.warning(f"無法顯示 {title}，資料格式異常: {e}")
            st.write("原始數據預覽:", raw_data)
    else:
        st.write(f"{title}: 暫無數據")

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("尚未載入數據，請等待 GitHub Actions 更新。")
        return

    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        target = st.selectbox("選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    current_target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(current_target, {})
    
    if info:
        st.subheader(f"分析目標: {current_target}")
        safe_display_df("institutional_daily", info, "三大法人 10 日買賣超")
        safe_display_df("broker_daily", info, "主力券商 10 日買賣超")
    else:
        st.write("請在側邊欄選擇股票。")

if __name__ == "__main__":
    main()
