import streamlit as st
import json
import os
import yfinance as yf
import plotly.express as px
import time
import random

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 讀取 JSON
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

st.subheader("🔍 手動查詢股票")
custom_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", placeholder="請輸入完整代號")

if st.button("取得即時股價"):
    if not custom_ticker:
        st.warning("請輸入代號")
    else:
        # 1. 優先從 JSON 找
        if custom_ticker in data:
            m = data[custom_ticker]
            st.success(f"已讀取自動化備份數據: {custom_ticker}")
            c1, c2, c3 = st.columns(3)
            c1.metric("即時股價", f"{m.get('price', 0):.2f}")
            c2.metric("本益比", f"{m.get('pe', 0):.2f}")
            c3.metric("EPS", f"{m.get('eps', 0):.2f}")
            st.info(f"🤖 AI 分析: {m.get('ai_prediction', '無分析資料')}")
        else:
            # 2. 只有沒資料才請求 API，加入隨機延遲繞過限制
            with st.spinner("正在連線 Yahoo Finance (嘗試繞過 API 限制)..."):
                try:
                    time.sleep(random.uniform(1.0, 3.0)) # 隨機延遲
                    ticker = yf.Ticker(custom_ticker)
                    # 使用 session 請求較穩定
                    hist = ticker.history(period="1mo")
                    if hist.empty:
                        st.error("查無此代號，或已被 Yahoo API 限制。請確認格式 (如 2330.TW)。")
                    else:
                        price = hist['Close'].iloc[-1]
                        st.success(f"已即時獲取 {custom_ticker} 資訊")
                        st.metric("即時股價", f"{price:.2f}")
                        st.warning("此標的未在自動化清單中，無 AI 分析數據。")
                        fig = px.line(hist, y="Close", title=f"{custom_ticker} 近期走勢")
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error("連線過於頻繁 (API Limit)。請稍候 1 分鐘再試，或建議將此標的加入 tickers.txt。")
