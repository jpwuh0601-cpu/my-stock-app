import streamlit as st
import json
import os
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 強力讀取函數：若檔案壞掉或讀不到，回傳空字典，絕不讓系統卡死
def load_data():
    if not os.path.exists("market_data.json"):
        return {}
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

data = load_data()

# 顯示介面
ticker_options = list(data.keys()) if data else ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
ticker_input = st.selectbox("請選擇監控標的", ticker_options)

# 若數據為空，顯示提示而非轉圈
if not data:
    st.error("系統數據尚未初始化，請確認 GitHub Actions 是否完成首次執行。")
else:
    m = data.get(ticker_input, {})
    st.metric("即時股價", f"{m.get('price', 0):.2f}")
    st.info(m.get("ai_prediction", "AI 分析引擎待命中..."))
    
    # 歷史走勢圖
    hist = yf.Ticker(ticker_input).history(period="1mo")
    if not hist.empty:
        fig = px.line(hist, y="Close", title=f"{ticker_input} 近期走勢")
        st.plotly_chart(fig, use_container_width=True)
