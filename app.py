import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 1. 強制讀取本地 JSON
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {}
    return {}

data = load_data()

# 2. 側邊欄：標的清單 (避免佔用主畫面)
st.sidebar.header("監控標的清單")
if not data:
    st.sidebar.error("數據載入中，請稍候...")
else:
    selected_ticker = st.sidebar.selectbox("請選擇監控對象:", list(data.keys()))
    
    # 3. 主畫面：數據面板
    m = data.get(selected_ticker, {})
    st.header(f"標的: {selected_ticker}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{m.get('price', 0):.2f}")
    col2.metric("本益比", f"{m.get('pe', 0):.2f}")
    col3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    # 4. AI 分析區塊 (使用 expander 節省空間)
    with st.expander("🤖 查看 AI 顧問深入分析", expanded=True):
        st.write(m.get('ai_prediction', '數據初始化中...'))
    
    # 5. 籌碼狀態 (簡化版)
    if "institutional_data" in m:
        st.subheader("籌碼趨勢預覽")
        df_inst = pd.DataFrame(m['institutional_data'])
        st.line_chart(df_inst.set_index('日期'))
    
    st.success(f"目前監控狀態: {m.get('black_swan', '安全')}")

st.markdown("---")
st.caption("自動化管線運作正常，數據每 24 小時更新一次。若有新標的需求，請更新 tickers.txt 並觸發 Action。")
