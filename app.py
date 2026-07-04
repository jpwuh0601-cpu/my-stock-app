import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 強制讀取本地 JSON
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

st.subheader("🔍 手動輸入標的 (自動從本地清單選取)")

if not data:
    st.error("系統尚未初始化，請確認 GitHub Actions 是否完成首次更新。")
else:
    # 這裡將手動輸入改為自動完成選單，完全避免對 Yahoo 發送請求
    ticker_options = list(data.keys())
    ticker_input = st.selectbox("請選擇或輸入標的代號:", ticker_options)

    if ticker_input in data:
        m = data[ticker_input]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("即時股價", f"{m.get('price', 0):.2f}")
        c2.metric("本益比", f"{m.get('pe', 0):.2f}")
        c3.metric("EPS", f"{m.get('eps', 0):.2f}")
        
        st.subheader("🤖 AI 顧問分析")
        st.info(m.get("ai_prediction", "分析中..."))
        
        st.warning(f"當前風險狀態: {m.get('black_swan', '安全')}")
    else:
        st.info("請從上方選單選擇一個標的進行分析。")

st.markdown("---")
st.caption("提示：若需要分析新股票，請編輯 `tickers.txt` 並手動執行 GitHub Action。此設計是為了避免 Yahoo Finance API 限制。")
