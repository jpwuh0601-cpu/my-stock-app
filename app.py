import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 強制讀取 JSON
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

# 只提供 JSON 清單中的選擇，確保不會發生 API 錯誤
if not data:
    st.error("目前無數據。請確認 GitHub Actions 是否已執行完畢。")
else:
    ticker_options = list(data.keys())
    ticker_input = st.selectbox("請選擇已監控標的", ticker_options)

    m = data[ticker_input]
    
    # 顯示數據
    c1, c2, c3 = st.columns(3)
    c1.metric("即時股價", f"{m.get('price', 0):.2f}")
    c2.metric("本益比", f"{m.get('pe', 0):.2f}")
    c3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    st.subheader("🤖 AI 顧問分析")
    st.info(m.get("ai_prediction", "分析中..."))
    
    st.warning(f"當前風險狀態: {m.get('black_swan', '安全')}")
