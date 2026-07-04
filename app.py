import streamlit as st
import json
import os
import plotly.express as px
import yfinance as yf

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 讀取 JSON 數據
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

# --- 新增：手動輸入區塊 ---
st.subheader("🔍 手動查詢股票")
custom_ticker = st.text_input("輸入股票代號 (例如: 0050.TW)", placeholder="按下 Enter 鍵搜尋")

# --- 邏輯：優先使用 JSON，若無則現場查詢 ---
target_ticker = custom_ticker if custom_ticker else "2330.TW"
ticker_obj = yf.Ticker(target_ticker)

if custom_ticker:
    st.info(f"正在為您即時查詢: {custom_ticker}...")
    info = ticker_obj.info
else:
    info = ticker_obj.info

# 顯示數據
if "currentPrice" in info:
    c1, c2, c3 = st.columns(3)
    c1.metric("即時股價", f"{info.get('currentPrice', 0):.2f}")
    c2.metric("本益比", f"{info.get('forwardPE', 0):.2f}")
    c3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
    
    # 若 JSON 中有預先分析好的資料，顯示 AI 分析
    if target_ticker in data:
        st.subheader("🤖 AI 顧問分析")
        st.info(data[target_ticker].get("ai_prediction", "分析中..."))
    else:
        st.warning("此標的目前未在自動化清單中，僅顯示即時市場數據。")

    # 股價走勢圖
    hist = ticker_obj.history(period="1mo")
    if not hist.empty:
        fig = px.line(hist, y="Close", title=f"{target_ticker} 近期走勢")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("查無此代號資訊，請確認代號是否包含 .TW 後綴 (例如 2330.TW)")
