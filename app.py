import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 強制讀取本地 JSON 資料，不向 Yahoo 發送 API 請求
@st.cache_data(ttl=60)
def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"無法讀取數據檔案: {e}")
    return {}

data = load_data()

st.subheader("🔍 監控標的儀表板")

if not data:
    st.error("目前沒有資料，請確認 GitHub Actions 是否已執行完畢。")
else:
    # 建立一個清單供使用者選擇
    ticker_options = list(data.keys())
    selected_ticker = st.selectbox("請選擇您的監控標的:", ticker_options)

    # 讀取對應的數據結構
    m = data.get(selected_ticker, {})
    
    # 呈現數據面板
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{m.get('price', 0):.2f}")
    col2.metric("本益比", f"{m.get('pe', 0):.2f}")
    col3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    # 顯示 AI 分析結果
    st.subheader("🤖 AI 顧問分析")
    st.info(m.get('ai_prediction', '數據初始化中...'))
    
    # 呈現風險狀態
    if m.get('black_swan') == "高風險":
        st.error(f"⚠️ 風險警示: {m.get('black_swan')}")
    else:
        st.success(f"✅ 當前狀態: {m.get('black_swan', '安全')}")

st.markdown("---")
st.markdown("💡 **操作提示**: 若要新增監控股票，請修改 `tickers.txt` 並執行一次 GitHub Actions。")
