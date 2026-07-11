import streamlit as st
import pandas as pd
import json
import os

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 讀取 JSON 數據的函數 (不直接呼叫 API)
@st.cache_data(ttl=3600)
def load_market_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

st.title("📈 專業股市決策儀表板")

# 讀取資料
data_source = load_market_data()
tickers = list(data_source.keys())

# 輸入區
selected_ticker = st.selectbox("選擇股票代號", tickers)

if selected_ticker:
    data = data_source[selected_ticker]
    
    # 1. 即時股價 (漲紅跌綠)
    change = data.get('change', 0)
    color = "red" if change >= 0 else "green"
    st.metric("即時股價", f"{data.get('price', 0):.2f}", f"{change:.2f}%")

    # 2. 基本指標
    col1, col2, col3 = st.columns(3)
    col1.metric("每股淨值", data.get('nav', 0))
    col2.metric("本益比", data.get('pe', 0))
    col3.metric("EPS", data.get('eps', 0))

    # 3. 三大法人十日明細 (HTML 渲染)
    st.markdown("### 4. 三大法人近十日買賣超明細")
    df_inst = pd.DataFrame(data['institutional_data'])
    st.table(df_inst)

    # 5. AI 分析與新聞
    st.markdown("### 5. AI 財報預測")
    st.info(data.get('ai_prediction', '無預測數據'))
    st.markdown("### 6. 即時新聞")
    st.write(data.get('news', '無最新新聞'))

    # 6. 黑天鵝
    st.markdown("### 7. 黑天鵝警示")
    st.warning(data.get('black_swan', '安全'))
