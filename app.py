import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def render_safe_df(raw_data, title):
    """強行將所有資料轉換為字串，徹底避免 TypeError"""
    if not raw_data:
        st.write(f"{title}: 暫無數據")
        return
    
    try:
        df = pd.DataFrame(raw_data)
        # 強制將所有欄位轉換為字串，避免 float 轉換錯誤
        df = df.astype(str)
        st.subheader(title)
        st.dataframe(df, width=None)
    except Exception as e:
        st.warning(f"無法轉換表格: {e}")
        st.write("原始數據:", raw_data)

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.info("資料載入中...")
        return

    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        target = st.selectbox("請選擇股票", tickers)
        if st.button("確定選股"):
            st.session_state.target = target
            
    current_target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(current_target, {})
    
    if info:
        st.subheader(f"分析目標: {current_target}")
        # 使用強行清洗後的渲染器
        render_safe_df(info.get("institutional_daily"), "三大法人 10 日買賣超")
        render_safe_df(info.get("broker_daily"), "主力券商 10 日買賣超")
    else:
        st.write("請在側邊欄選擇股票並確認。")

if __name__ == "__main__":
    main()
