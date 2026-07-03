import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if not os.path.exists("market_data.json"):
        return {}
    with open("market_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("數據載入中，請等待自動化排程更新。")
        return

    # 回測檢核機制
    last_updated_str = data.get("last_updated", "2000-01-01 00:00:00")
    last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
    
    if datetime.now() - last_updated > timedelta(hours=24):
        st.error(f"⚠️ 數據來源已過期 (最後更新: {last_updated_str})，請手動觸發自動化更新！")
    else:
        st.success(f"✅ 數據更新正常 (最後更新: {last_updated_str})")

    # 側邊欄
    with st.sidebar.form(key='ticker_form'):
        tickers = [t for t in data.keys() if t != "last_updated"]
        selected_ticker = st.selectbox("請選擇股票代號", tickers)
        submit_button = st.form_submit_button(label='確定分析')

    if submit_button:
        info = data.get(selected_ticker, {})
        st.header(f"監控目標: {selected_ticker}")
        st.metric("即時股價", f"{float(info.get('price', 0)):,.2f}")

        # 財報數據顯示
        col1, col2, col3 = st.columns(3)
        col1.metric("每股淨值 (BVPS)", f"{info.get('bvps', 0):,.2f}")
        col2.metric("本益比 (PE)", f"{info.get('pe', 0):,.2f}")
        col3.metric("EPS", f"{info.get('eps', 0):,.2f}")

        # 走勢圖
        history = info.get("history", [])
        if history:
            df = pd.DataFrame(history)
            fig = px.line(df, x="Date", y="Close", title="近一月股價走勢")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🤖 AI 財報預測分析")
        st.info(info.get("ai_prediction", "暫無分析數據"))

if __name__ == "__main__":
    main()
