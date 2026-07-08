import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

# CSS 樣式
st.markdown("""
    <style>
    .price-up { color: #ff4b4b; font-weight: bold; }
    .price-down { color: #00cc96; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def load_data():
    """載入本地 JSON 資料"""
    try:
        if os.path.exists("market_data.json"):
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def main():
    st.title("📈 專業股市決策儀表板")
    data = load_data()

    # 1. 輸入股票代號
    ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.button("查詢分析數據"):
        st.session_state.current_ticker = ticker_input

    ticker = st.session_state.get("current_ticker", ticker_input)
    
    # 邏輯：優先讀取本地 JSON，若無則呼叫即時 API
    s = {}
    if ticker in data:
        s = data[ticker]
        st.success("已載入本地分析數據")
    else:
        with st.spinner("本地無資料，正在即時從網路擷取..."):
            realtime = fetch_stock_data(ticker)
            if "error" not in realtime:
                info = realtime.get("info", {})
                s = {
                    "price": realtime.get("price", 0),
                    "nav": info.get("bookValue", "N/A"),
                    "pe": info.get("trailingPE", "N/A"),
                    "eps": info.get("trailingEps", "N/A"),
                    "change": 0, "kd": "N/A", "macd": "N/A", "rsi": "N/A"
                }
            else:
                st.error("無法取得即時資料，請確認代號正確或網路連線。")
    
    if s:
        # 顯示漲跌顏色
        change = s.get('change', 0)
        color_class = "price-up" if change >= 0 else "price-down"
        st.markdown(f"### 即時股價: <span class='{color_class}'>{s.get('price', 0)} ({change:+.2f})</span>", unsafe_allow_html=True)

        # 2. 每股淨值、本益比、EPS
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", f"{s.get('nav', 0)}")
        c2.metric("本益比", f"{s.get('pe', 0)}")
        c3.metric("EPS", f"{s.get('eps', 0)}")

        # 3-10. 顯示剩餘指標 (安全性處理)
        st.subheader("📊 技術分析與籌碼面")
        tech_data = {"指標": ["KD", "MACD", "RSI"], "數值": [s.get('kd', 'N/A'), s.get('macd', 'N/A'), s.get('rsi', 'N/A')]}
        st.table(pd.DataFrame(tech_data))
        
        st.subheader("🔮 AI 財報預測")
        st.success(s.get('ai_prediction', '數據分析中...'))

if __name__ == "__main__":
    main()
