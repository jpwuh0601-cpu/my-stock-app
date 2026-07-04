import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 讀取 JSON 數據
def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_data()

if not data:
    st.error("目前沒有資料，請檢查 GitHub Actions 是否正確寫入 market_data.json。")
else:
    # 建立選單
    tickers = list(data.keys())
    selected = st.selectbox("請選擇監控標的:", tickers)
    
    # 提取該標的數據
    info = data.get(selected, {})
    
    # UI 呈現
    col1, col2, col3 = st.columns(3)
    col1.metric("即時價格", f"{info.get('price', 0):.2f}")
    col2.metric("本益比", f"{info.get('pe', 0):.2f}")
    col3.metric("EPS", f"{info.get('eps', 0):.2f}")
    
    st.subheader("🤖 AI 分析結果")
    st.info(info.get('ai_prediction', '分析中...'))
    
    st.markdown("---")
    st.caption("✅ 數據來自 GitHub Actions 自動更新系統")
