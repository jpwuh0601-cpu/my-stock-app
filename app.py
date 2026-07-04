import streamlit as st
import json
import os
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 1. 載入 JSON 資料
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

# 2. 手動輸入區塊
st.subheader("🔍 手動查詢股票")
custom_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", placeholder="請輸入代號後點擊下方按鈕")

if st.button("取得即時股價"):
    if not custom_ticker:
        st.warning("請先輸入有效的股票代號。")
    else:
        with st.spinner(f"正在連線查詢 {custom_ticker}..."):
            try:
                # 優先檢查是否在清單內
                if custom_ticker in data:
                    m = data[custom_ticker]
                    st.success(f"已從資料庫讀取 {custom_ticker} 資訊")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("即時股價", f"{m.get('price', 0):.2f}")
                    c2.metric("本益比", f"{m.get('pe', 0):.2f}")
                    c3.metric("EPS", f"{m.get('eps', 0):.2f}")
                    st.info(f"🤖 AI 分析: {m.get('ai_prediction', '無分析數據')}")
                else:
                    # 現場查詢機制
                    ticker = yf.Ticker(custom_ticker)
                    info = ticker.info
                    price = info.get("currentPrice") or info.get("regularMarketPrice")
                    
                    if price:
                        st.success(f"已即時獲取 {custom_ticker} 資訊")
                        st.metric("即時股價", f"{price:.2f}")
                        st.warning("此標的未在自動化清單中，暫無 AI 分析數據。")
                    else:
                        st.error("查無此代號，請檢查是否包含 .TW 後綴。")
                
                # 繪圖
                hist = yf.Ticker(custom_ticker).history(period="1mo")
                if not hist.empty:
                    fig = px.line(hist, y="Close", title=f"{custom_ticker} 近期走勢")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"查詢失敗，可能是請求過於頻繁 (API Limit)。請稍候再試或將此標的加入 tickers.txt。")
