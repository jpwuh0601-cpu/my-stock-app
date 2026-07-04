import streamlit as st
import json
import os
import plotly.express as px
import yfinance as yf
import time

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

# 讀取 JSON 數據
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

data = load_data()

# --- 手動查詢區塊 ---
st.subheader("🔍 手動查詢股票")
custom_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", placeholder="請輸入代號並按下 Enter")

# 處理輸入：若未輸入，預設顯示 2330.TW
target_ticker = custom_ticker.strip() if custom_ticker else "2330.TW"

# 確保輸入符合 Yahoo Finance 格式
if target_ticker and "." not in target_ticker and target_ticker.isdigit():
    target_ticker += ".TW"

if st.button("取得即時股價"):
    with st.spinner(f"正在連線 Yahoo Finance 查詢 {target_ticker}..."):
        try:
            # 建立物件並強制更新
            ticker_obj = yf.Ticker(target_ticker)
            # 使用 fast_info 或 info 獲取價格
            info = ticker_obj.info
            
            # 優先獲取 currentPrice，若無則嘗試正規價格
            price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")

            if price:
                st.success(f"已成功載入 {target_ticker} 資訊")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("即時股價", f"{price:.2f}")
                c2.metric("本益比", f"{info.get('forwardPE', 0) or 0:.2f}")
                c3.metric("EPS", f"{info.get('trailingEps', 0) or 0:.2f}")
                
                # 若 JSON 中有預先分析好的資料，顯示 AI 分析
                if target_ticker in data:
                    st.subheader("🤖 AI 顧問分析")
                    st.info(data[target_ticker].get("ai_prediction", "AI 分析數據待命中..."))
                
                # 繪製走勢圖
                hist = ticker_obj.history(period="1mo")
                if not hist.empty:
                    fig = px.line(hist, y="Close", title=f"{target_ticker} 近期走勢")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"無法取得代號 '{target_ticker}' 的市場價格，請確認代號是否正確。")
        
        except Exception as e:
            st.error(f"查詢發生錯誤: {str(e)}")
