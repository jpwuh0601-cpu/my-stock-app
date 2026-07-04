import streamlit as st
import json
import os
import datetime

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 獲取檔案最後修改時間
def get_file_age(file_path):
    if os.path.exists(file_path):
        mtime = os.path.getmtime(file_path)
        return datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    return "未知"

@st.cache_data(ttl=60)
def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_data()
last_update = get_file_age("market_data.json")

# 顯示最後更新時間
st.caption(f"🕒 數據最後更新時間: {last_update} (GitHub Actions)")

if not data:
    st.error("系統初始化中，請稍候。")
else:
    # 標的選擇器
    ticker_options = list(data.keys())
    selected_ticker = st.selectbox("選擇監控標的:", ticker_options)
    
    m = data.get(selected_ticker, {})
    
    # 專業數據儀表板
    col1, col2, col3 = st.columns(3)
    col1.metric("價格", f"{m.get('price', 0):.2f}")
    col2.metric("本益比 (PE)", f"{m.get('pe', 0):.2f}")
    col3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    # AI 分析框
    st.markdown("---")
    st.subheader("🤖 AI 深度分析")
    st.write(m.get('ai_prediction', '正在進行 AI 運算...'))
    
    # 風險指示
    status = m.get('black_swan', '安全')
    if status == "安全":
        st.success(f"✅ 狀態評估: {status}")
    else:
        st.warning(f"⚠️ 狀態評估: {status}")
