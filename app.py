import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# GitHub RAW URL
RAW_URL = "https://raw.githubusercontent.com/jpwuh0601-cpu/my-stock-app/main/market_data.json"

@st.cache_data(ttl=3600)
def load_json_data():
    try:
        response = requests.get(RAW_URL, timeout=10)
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

# 載入數據
all_data = load_json_data()

# 側邊欄選擇器
available_tickers = list(all_data.keys())
ticker = st.sidebar.selectbox("請選擇已分析的股票", options=available_tickers if available_tickers else ["無數據"])

if st.sidebar.button("查詢分析數據"):
    if ticker in all_data:
        data = all_data[ticker]
        
        # 顯示 8 項關鍵指標
        st.subheader(f"📊 {ticker} 分析儀表板")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0):.2f}")
        col2.metric("漲跌幅", f"{data.get('change', 0):.2%}")
        col3.metric("每股淨額", f"{data.get('nav', 0):.2f}")
        col4.metric("本益比", f"{data.get('pe', 0):.2f}")
        
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("每股盈餘", f"{data.get('eps', 0):.2f}")
        col6.metric("融資餘額比", f"{data.get('margin_ratio', 0):.2%}")
        
        # 視覺化圖表：法人籌碼長條圖
        st.subheader("🤖 AI 分析與籌碼視覺化")
        st.info(data.get("ai_prediction", "AI 正在分析中..."))
        
        # 使用 Plotly 繪製法人籌碼
        inst_data = data.get("institutional_data", [])
        if inst_data:
            df = pd.DataFrame(inst_data)
            fig = go.Figure(data=[
                go.Bar(name='外資', x=df['日期'], y=df['外資']),
                go.Bar(name='投信', x=df['日期'], y=df['投信']),
                go.Bar(name='自營商', x=df['日期'], y=df['自營商'])
            ])
            fig.update_layout(barmode='group', title='近期法人買賣超')
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.error("查無資料。請確認 GitHub Actions 是否已成功更新 market_data.json。")
